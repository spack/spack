# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

if sys.platform == "win32":
    pytest.skip("Jobserver tests are not supported on Windows", allow_module_level=True)

import fcntl
import os
import pathlib
import stat

from spack.new_installer_posix import (
    PosixJobServer,
    create_jobserver_fifo,
    get_jobserver_config,
    open_existing_jobserver_fifo,
)
from spack.spec import Spec


class TestGetJobserverConfig:
    """Test parsing of MAKEFLAGS for jobserver configuration."""

    def test_empty_makeflags(self):
        """Empty MAKEFLAGS should return None."""
        assert get_jobserver_config("") is None

    def test_no_jobserver_flag(self):
        """MAKEFLAGS without jobserver flag should return None."""
        assert get_jobserver_config(" -j4 --silent") is None

    def test_fifo_format_new(self):
        """Parse new FIFO format"""
        assert get_jobserver_config(" -j4 --jobserver-auth=fifo:/tmp/my_fifo") == "/tmp/my_fifo"

    def test_pipe_format_new(self):
        """Parse new pipe format"""
        assert get_jobserver_config(" -j4 --jobserver-auth=3,4") == (3, 4)

    def test_pipe_format_old(self):
        """Parse old pipe format (on old versions of gmake this was not publicized)"""
        assert get_jobserver_config(" -j4 --jobserver-fds=5,6") == (5, 6)

    def test_multiple_flags_last_wins(self):
        """When multiple jobserver flags exist, last one wins."""
        makeflags = " --jobserver-fds=3,4 --jobserver-auth=fifo:/tmp/fifo --jobserver-auth=7,8"
        assert get_jobserver_config(makeflags) == (7, 8)

    def test_invalid_format(self):
        assert get_jobserver_config(" --jobserver-auth=3") is None
        assert get_jobserver_config(" --jobserver-auth=a,b") is None
        assert get_jobserver_config(" --jobserver-auth=3,b") is None
        assert get_jobserver_config(" --jobserver-auth=3,4,5") is None
        assert get_jobserver_config(" --jobserver-auth=") is None


class TestCreateJobserverFifo:
    """Test FIFO creation for jobserver."""

    def test_creates_fifo(self):
        """Should create a FIFO with correct properties."""
        r, w, path = create_jobserver_fifo(4)
        try:
            assert os.path.exists(path)
            assert stat.S_ISFIFO(os.stat(path).st_mode)
            assert (os.stat(path).st_mode & 0o777) == 0o600
            assert fcntl.fcntl(r, fcntl.F_GETFD) != -1
            assert fcntl.fcntl(w, fcntl.F_GETFD) != -1
            assert fcntl.fcntl(r, fcntl.F_GETFL) & os.O_NONBLOCK
        finally:
            os.close(r)
            os.close(w)
            os.unlink(path)
            os.rmdir(os.path.dirname(path))

    def test_writes_correct_tokens(self):
        """Should write num_jobs - 1 tokens."""
        r, w, path = create_jobserver_fifo(5)
        try:
            assert os.read(r, 10) == b"++++"  # 4 tokens for 5 jobs
        finally:
            os.close(r)
            os.close(w)
            os.unlink(path)
            os.rmdir(os.path.dirname(path))

    def test_single_job_no_tokens(self):
        """Single job should write 0 tokens."""
        r, w, path = create_jobserver_fifo(1)
        try:
            with pytest.raises(BlockingIOError):
                os.read(r, 10)  # No tokens for 1 job
        finally:
            os.close(r)
            os.close(w)
            os.unlink(path)
            os.rmdir(os.path.dirname(path))


class TestOpenExistingJobserverFifo:
    """Test opening existing jobserver FIFOs."""

    def test_opens_existing_fifo(self, tmp_path: pathlib.Path):
        """Should successfully open an existing FIFO."""
        fifo_path = str(tmp_path / "test_fifo")
        os.mkfifo(fifo_path, 0o600)

        result = open_existing_jobserver_fifo(fifo_path)
        assert result is not None

        r, w = result
        assert fcntl.fcntl(r, fcntl.F_GETFD) != -1
        assert fcntl.fcntl(w, fcntl.F_GETFD) != -1
        assert fcntl.fcntl(r, fcntl.F_GETFL) & os.O_NONBLOCK

        os.close(r)
        os.close(w)

    def test_returns_none_for_missing_fifo(self, tmp_path: pathlib.Path):
        """Should return None if FIFO doesn't exist."""
        result = open_existing_jobserver_fifo(str(tmp_path / "nonexistent_fifo"))
        assert result is None


#: Constant that's larger than the number of jobs used in tests.
ALL_TOKENS = 100


class TestJobServer:
    """Test PosixJobServer class functionality."""

    def test_creates_new_jobserver(self):
        """Should create a new FIFO-based jobserver when none exists."""
        js = PosixJobServer(4)

        try:
            assert js.created is True
            assert js.fifo_path is not None
            assert os.path.exists(js.fifo_path)
            assert js.tokens_acquired == 0
            assert fcntl.fcntl(js.r, fcntl.F_GETFD) != -1
            assert fcntl.fcntl(js.w, fcntl.F_GETFD) != -1
        finally:
            js.close()

    def test_attaches_to_existing_fifo(self):
        """Should attach to existing FIFO jobserver from environment."""
        js1 = PosixJobServer(4)
        assert js1.fifo_path

        try:
            fifo_config = get_jobserver_config(f" -j4 --jobserver-auth=fifo:{js1.fifo_path}")
            assert fifo_config == js1.fifo_path

            result = open_existing_jobserver_fifo(js1.fifo_path)
            assert result is not None

            r, w = result
            os.close(r)
            os.close(w)

        finally:
            js1.close()

    def test_acquire_tokens(self):
        """Should acquire tokens from jobserver."""
        js = PosixJobServer(5)

        try:
            assert js.acquire(2) == 2
            assert js.tokens_acquired == 2

            assert js.acquire(2) == 2
            assert js.tokens_acquired == 4

            assert js.acquire(2) == 0
            assert js.tokens_acquired == 4

        finally:
            js.close()

    def test_release_tokens(self):
        """Should release tokens back to jobserver."""
        js = PosixJobServer(5)

        try:
            assert js.acquire(2) == 2
            assert js.tokens_acquired == 2

            js.release()
            assert js.tokens_acquired == 1

            assert js.acquire(1) == 1
            assert js.tokens_acquired == 2

        finally:
            js.close()

    def test_release_without_tokens_is_noop(self):
        """Releasing without acquired tokens should be a no-op."""
        js = PosixJobServer(4)

        try:
            assert js.tokens_acquired == 0
            js.release()
            assert js.tokens_acquired == 0
        finally:
            js.close()

    def test_makeflags_fifo_gmake_44(self):
        """Should return FIFO format for gmake >= 4.4."""
        js = PosixJobServer(8)

        try:
            flags, data = js.makeflags_and_data(Spec("gmake@=4.4"))
            assert flags == f" -j8 --jobserver-auth=fifo:{js.fifo_path}"
            assert data is None
        finally:
            js.close()

    def test_makeflags_pipe_gmake_40(self):
        """Should return pipe format for gmake 4.0-4.3."""
        js = PosixJobServer(8)

        try:
            flags, data = js.makeflags_and_data(Spec("gmake@=4.0"))
            assert flags == f" -j8 --jobserver-auth={js.r},{js.w}"
            assert data == (js.r_conn, js.w_conn)
        finally:
            js.close()

    def test_makeflags_old_format_gmake_3(self):
        """Should return old --jobserver-fds format for gmake < 4.0."""
        js = PosixJobServer(8)

        try:
            flags, data = js.makeflags_and_data(Spec("gmake@=3.9"))
            assert flags == f" -j8 --jobserver-fds={js.r},{js.w}"
            assert data == (js.r_conn, js.w_conn)
        finally:
            js.close()

    def test_makeflags_no_gmake(self):
        """Should return FIFO format when no gmake (modern default)."""
        js = PosixJobServer(6)

        try:
            flags, data = js.makeflags_and_data(None)
            assert flags == f" -j6 --jobserver-auth=fifo:{js.fifo_path}"
            assert data is None
        finally:
            js.close()

    def test_close_removes_created_fifo(self):
        """Should remove FIFO and directory if created by this instance."""
        js = PosixJobServer(4)
        fifo_path = js.fifo_path
        assert fifo_path and os.path.exists(fifo_path)
        js.close()
        assert not os.path.exists(os.path.dirname(fifo_path))

    def test_file_descriptors_are_inheritable(self):
        """Should set file descriptors as inheritable for child processes."""
        js = PosixJobServer(4)

        try:
            assert os.get_inheritable(js.r)
            assert os.get_inheritable(js.w)
        finally:
            js.close()

    def test_connection_objects_exist(self):
        """Should create Connection objects for fd inheritance."""
        js = PosixJobServer(4)

        try:
            assert js.r_conn is not None and js.r_conn.fileno() == js.r
            assert js.w_conn is not None and js.w_conn.fileno() == js.w
        finally:
            js.close()

    def test_close_warns_when_spack_holds_tokens(self):
        """Should warn when Spack closes the jobserver while still holding acquired tokens."""
        js = PosixJobServer(4)
        js.acquire(1)  # Spack acquires a token without releasing it
        with pytest.warns(UserWarning, match="Spack failed to release jobserver tokens"):
            js.close()

    def test_close_warns_when_subprocess_holds_tokens(self):
        """Should warn when a subprocess acquired a token but never released it."""
        js1 = PosixJobServer(4)
        os.read(js1.r, 1)  # A subprocess acquires a token without releasing it
        with pytest.warns(UserWarning, match="1 jobserver token was not released"):
            js1.close()

        js2 = PosixJobServer(4)
        os.read(js2.r, 2)  # A subprocess acquires two tokens without releasing them
        with pytest.warns(UserWarning, match="2 jobserver tokens were not released"):
            js2.close()

    def test_has_target_parallelism(self):
        """has_target_parallelism() should be True initially."""
        js = PosixJobServer(4)
        try:
            assert js.has_target_parallelism() is True
            js.target_jobs = js.num_jobs - 1
            assert js.has_target_parallelism() is False
        finally:
            js.close()

    def test_increase_parallelism_not_created(self):
        """increase_parallelism() should be a no-op when not self.created."""
        # Simulate an externally attached jobserver by patching created after construction.
        js = PosixJobServer(3)
        try:
            original_num = js.num_jobs
            original_target = js.target_jobs
            js.created = False
            js.increase_parallelism()
            assert js.num_jobs == original_num
            assert js.target_jobs == original_target
            js.decrease_parallelism()
            assert js.num_jobs == original_num
            assert js.target_jobs == original_target
        finally:
            js.created = True  # restore so close() works
            js.close()

    def test_increase_parallelism(self):
        """increase_parallelism() should increment num_jobs and target_jobs and add a token."""
        js = PosixJobServer(3)
        try:
            original_num = js.num_jobs
            original_target = js.target_jobs
            js.increase_parallelism()
            assert js.num_jobs == original_num + 1
            assert js.target_jobs == original_target + 1
            # Verify the "js.num_jobs - 1 tokens in the pipe" invariant.
            assert js.acquire(ALL_TOKENS) + 1 == js.num_jobs
        finally:
            js.close()

    def test_decrease_parallelism_at_floor(self):
        """decrease_parallelism() should not go below target_jobs == 1."""
        js = PosixJobServer(1)
        try:
            # target_jobs starts at 1
            assert js.target_jobs == 1
            js.decrease_parallelism()
            assert js.target_jobs == 1
        finally:
            js.close()

    def test_decrease_parallelism_token_available(self):
        """When pipe has tokens, decrease_parallelism discards one immediately."""
        js = PosixJobServer(3)
        try:
            # 3-job server starts with 2 tokens in the pipe.
            original_num = js.num_jobs
            js.decrease_parallelism()
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num - 1
            assert js.acquire(ALL_TOKENS) + 1 == js.num_jobs
        finally:
            js.close()

    def test_decrease_parallelism_no_token_available(self):
        """When all tokens are held, decrease_parallelism defers the discard.
        A subsequent increase cancels the pending decrease instead of adding a token."""
        js = PosixJobServer(3)
        try:
            # Drain the pipe so no tokens are available for immediate discard.
            assert js.acquire(ALL_TOKENS) == js.num_jobs - 1
            original_num = js.num_jobs
            js.decrease_parallelism()
            # target_jobs decremented but num_jobs unchanged (no token to discard yet).
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num
            # increase should cancel the pending decrease, not write a new token.
            js.increase_parallelism()
            assert js.target_jobs == original_num
            assert js.num_jobs == original_num
        finally:
            js.close()

    def test_maybe_discard_tokens_noop_at_target(self):
        """maybe_discard_tokens() should be a no-op when num_jobs == target_jobs."""
        js = PosixJobServer(3)
        try:
            original_num = js.num_jobs
            js._maybe_discard_tokens()  # to_discard == 0
            assert js.num_jobs == original_num
        finally:
            js.close()

    def test_maybe_discard_tokens_discards_when_available(self):
        """maybe_discard_tokens() should consume tokens from the pipe."""
        js = PosixJobServer(4)
        try:
            # Manually set target lower to create a discard requirement.
            js.target_jobs = js.num_jobs - 2
            original_num = js.num_jobs
            js._maybe_discard_tokens()
            assert js.num_jobs < original_num
        finally:
            js.close()

    def test_maybe_discard_tokens_noop_on_blocking(self):
        """maybe_discard_tokens() should not raise when pipe is empty."""
        js = PosixJobServer(3)
        try:
            # Drain all tokens from the pipe (simulates subprocesses holding them).
            assert js.acquire(ALL_TOKENS) == js.num_jobs - 1
            original_num = js.num_jobs
            # Artificially lower target so a discard is requested, but pipe is empty.
            js.target_jobs = js.num_jobs - 1
            js._maybe_discard_tokens()  # Should not raise; num_jobs unchanged.
            assert js.num_jobs == original_num
        finally:
            js.close()

    def test_release_discards_token_when_target_below_num(self):
        """release() should discard a token (not return it) when target_jobs < num_jobs."""
        js = PosixJobServer(4)
        try:
            # Acquire a token.
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
            # Manually lower target to simulate a pending decrease.
            js.target_jobs = js.num_jobs - 1
            original_num = js.num_jobs
            # Drain the free tokens from the pipe so we can count them after.
            drained = os.read(js.r, ALL_TOKENS)
            # Release should discard the token (decrement num_jobs) instead of writing to pipe.
            js.release()
            assert js.tokens_acquired == 0
            assert js.num_jobs == original_num - 1
            # Pipe should remain empty (nothing written back).
            with pytest.raises(BlockingIOError):
                os.read(js.r, 1)
        finally:
            # Restore drained tokens so close() can clean up cleanly.
            os.write(js.w, drained)
            js.close()
