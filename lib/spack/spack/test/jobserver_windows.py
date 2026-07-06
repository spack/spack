# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ctypes
import sys

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only", allow_module_level=True)

from spack.new_installer_windows import (
    WAIT_OBJECT_0,
    WindowsJobServer,
    get_jobserver_semaphore_name,
)

#: Larger than the number of jobs in any test; used to drain the semaphore completely.
ALL_TOKENS = 100


def _drain(js: WindowsJobServer) -> int:
    """Acquire all available tokens; return the count acquired."""
    count = 0
    for _ in range(ALL_TOKENS):
        if not js.acquire(1):
            break
        count += 1
    return count


class TestGetJobserverSemaphoreName:
    def test_empty_makeflags(self):
        assert get_jobserver_semaphore_name("") is None

    def test_no_jobserver_flag(self):
        assert get_jobserver_semaphore_name(" -j4 --silent") is None

    def test_fifo_format_skipped(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=fifo:/tmp/fifo") is None

    def test_pipe_comma_format_skipped(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=3,4") is None

    def test_plain_name_matched(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=my-semaphore") == "my-semaphore"

    def test_spack_pid_style_name(self):
        assert (
            get_jobserver_semaphore_name(" -j4 --jobserver-auth=spack-jobserver-1234")
            == "spack-jobserver-1234"
        )

    def test_multiple_flags_last_plain_wins(self):
        makeflags = (
            " --jobserver-auth=fifo:/tmp/fifo --jobserver-auth=3,4"
            " --jobserver-auth=spack-jobserver-99"
        )
        assert get_jobserver_semaphore_name(makeflags) == "spack-jobserver-99"

    def test_plain_before_pipe_returns_plain(self):
        makeflags = " --jobserver-auth=spack-jobserver-1 --jobserver-auth=3,4"
        # last win: 3,4 is a pipe format (skipped), so the last *plain* is spack-jobserver-1
        assert get_jobserver_semaphore_name(makeflags) == "spack-jobserver-1"

    def test_no_leading_space_matched(self):
        # MAKEFLAGS may start directly with --jobserver-auth (no preceding -j flag)
        assert get_jobserver_semaphore_name("--jobserver-auth=bare-name") == "bare-name"


class TestWindowsJobServer:
    def test_creates_new_jobserver(self):
        js = WindowsJobServer(4)
        try:
            assert js._created is True
            assert js.semaphore_name.startswith("spack-jobserver-")
            assert js.semaphore != 0
        finally:
            js.close()

    def test_initial_token_count(self):
        js = WindowsJobServer(4)
        try:
            assert _drain(js) == js.num_jobs - 1
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_single_job_server_has_no_tokens(self):
        js = WindowsJobServer(1)
        try:
            assert js.acquire(1) == 0
        finally:
            js.close()

    def test_attaches_to_existing_semaphore(self, monkeypatch):
        js1 = WindowsJobServer(4)
        try:
            monkeypatch.setenv("MAKEFLAGS", f" -j4 --jobserver-auth={js1.semaphore_name}")
            js2 = WindowsJobServer(4)
            try:
                assert js2._created is False
                assert js2.semaphore_name == js1.semaphore_name
                assert js2.semaphore != 0
            finally:
                js2.close()
        finally:
            js1.close()

    def test_attaches_shares_token_pool(self, monkeypatch):
        js1 = WindowsJobServer(3)  # 2 tokens
        try:
            monkeypatch.setenv("MAKEFLAGS", f" -j3 --jobserver-auth={js1.semaphore_name}")
            js2 = WindowsJobServer(3)
            try:
                assert js2.acquire(1) == 1
                assert js2.acquire(1) == 1
                assert js2.acquire(1) == 0  # pool exhausted
                assert js1.acquire(1) == 0  # js1 sees the same empty pool
            finally:
                js2.release()
                js2.release()
                js2.close()
        finally:
            js1.close()

    def test_makeflags_round_trip(self):
        js = WindowsJobServer(4)
        try:
            flags, _ = js.makeflags_and_data(None)
            assert get_jobserver_semaphore_name(flags) == js.semaphore_name
        finally:
            js.close()

    def test_acquire(self):
        js = WindowsJobServer(5)
        try:
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 2
        finally:
            js.release()
            js.release()
            js.close()

    def test_acquire_returns_zero_when_empty(self):
        js = WindowsJobServer(2)
        try:
            # 2-job server has 1 token; second acquire should fail
            assert js.acquire(1) == 1
            assert js.acquire(1) == 0
            assert js.tokens_acquired == 1
        finally:
            js.release()
            js.close()

    def test_release(self):
        js = WindowsJobServer(5)
        try:
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
            js.release()
            assert js.tokens_acquired == 0
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
        finally:
            js.release()
            js.close()

    def test_makeflags_format(self):
        js = WindowsJobServer(8)
        try:
            flags, _ = js.makeflags_and_data(None)
            assert flags == f" -j8 --jobserver-auth={js.semaphore_name}"
        finally:
            js.close()

    def test_close_closes_handle(self):
        js = WindowsJobServer(4)
        assert js.semaphore != 0
        js.close()
        # After CloseHandle, WaitForSingleObject returns WAIT_FAILED (0xFFFFFFFF as DWORD)
        result = ctypes.windll.kernel32.WaitForSingleObject(js.semaphore, 0)
        assert result == 0xFFFFFFFF

    def test_close_warns_spack_holds_tokens(self):
        js = WindowsJobServer(4)
        js.acquire(1)
        with pytest.warns(UserWarning, match="Spack failed to release jobserver tokens"):
            js.close()

    def test_close_warns_subprocess_holds_tokens_one(self):
        js = WindowsJobServer(4)
        # Simulate a subprocess consuming a token directly (bypassing acquire())
        k32 = ctypes.windll.kernel32
        assert k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        with pytest.warns(UserWarning, match="1 jobserver tokens were not released"):
            js.close()

    def test_close_warns_subprocess_holds_tokens_two(self):
        js = WindowsJobServer(4)
        k32 = ctypes.windll.kernel32
        assert k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        assert k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        with pytest.warns(UserWarning, match="2 jobserver tokens were not released"):
            js.close()

    def test_increase_parallelism_not_created(self):
        js = WindowsJobServer(3)
        try:
            original_num = js.num_jobs
            original_target = js.target_jobs
            js._created = False
            js.increase_parallelism()
            assert js.num_jobs == original_num
            assert js.target_jobs == original_target
            js.decrease_parallelism()
            assert js.num_jobs == original_num
            assert js.target_jobs == original_target
        finally:
            js.close()

    def test_increase_parallelism(self):
        js = WindowsJobServer(3)
        try:
            original_num = js.num_jobs
            original_target = js.target_jobs
            js.increase_parallelism()
            assert js.num_jobs == original_num + 1
            assert js.target_jobs == original_target + 1
            # Verify the "num_jobs - 1 tokens in the semaphore" invariant.
            assert _drain(js) + 1 == js.num_jobs
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_decrease_parallelism_at_floor(self):
        js = WindowsJobServer(1)
        try:
            assert js.target_jobs == 1
            js.decrease_parallelism()
            assert js.target_jobs == 1
        finally:
            js.close()

    def test_decrease_parallelism_token_available(self):
        js = WindowsJobServer(3)
        try:
            original_num = js.num_jobs
            js.decrease_parallelism()
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num - 1
            assert _drain(js) + 1 == js.num_jobs
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_decrease_parallelism_no_token_available(self):
        js = WindowsJobServer(3)
        try:
            # Drain the semaphore so no tokens are available for immediate discard.
            assert _drain(js) == js.num_jobs - 1
            original_num = js.num_jobs
            js.decrease_parallelism()
            # target_jobs decremented but num_jobs unchanged (no token to discard yet).
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num
            # increase should cancel the pending decrease, not add a new token.
            js.increase_parallelism()
            assert js.target_jobs == original_num
            assert js.num_jobs == original_num
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_maybe_discard_tokens_discards_when_available(self):
        js = WindowsJobServer(4)
        try:
            js.target_jobs = js.num_jobs - 2
            js._maybe_discard_tokens()
            assert js.num_jobs == js.target_jobs
        finally:
            js.close()

    def test_maybe_discard_tokens_noop_when_semaphore_empty(self):
        js = WindowsJobServer(3)
        try:
            assert _drain(js) == js.num_jobs - 1
            original_num = js.num_jobs
            js.target_jobs = js.num_jobs - 1
            js._maybe_discard_tokens()
            assert js.num_jobs == original_num
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_release_discards_token_when_target_below_num(self):
        js = WindowsJobServer(4)
        k32 = ctypes.windll.kernel32
        try:
            assert js.acquire(1) == 1
            js.target_jobs = js.num_jobs - 1
            original_num = js.num_jobs
            # Drain remaining free tokens from semaphore so we can verify nothing is put back.
            drained = 0
            while k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0:
                drained += 1
            js.release()
            assert js.tokens_acquired == 0
            assert js.num_jobs == original_num - 1
            # Semaphore should still be empty (token was discarded, not returned).
            assert k32.WaitForSingleObject(js.semaphore, 0) != WAIT_OBJECT_0
        finally:
            # Restore drained tokens so close() can clean up cleanly.
            if drained > 0:
                k32.ReleaseSemaphore(js.semaphore, drained, None)
            js.close()


