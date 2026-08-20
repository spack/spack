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
import selectors
import stat

from spack.installer.base import NoMakeflags
from spack.installer.posix import (
    FifoMakeflags,
    PipeMakeflags,
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

    def test_pipe_format_new_not_recognized(self):
        """Pipe-based jobservers aren't recognized: there's no path to hand a build process."""
        assert get_jobserver_config(" -j4 --jobserver-auth=3,4") is None

    def test_pipe_format_old_not_recognized(self):
        """Old-style --jobserver-fds is likewise not recognized."""
        assert get_jobserver_config(" -j4 --jobserver-fds=5,6") is None

    def test_multiple_flags_last_wins(self):
        """When multiple jobserver flags exist, last one wins."""
        makeflags = " --jobserver-fds=3,4 --jobserver-auth=fifo:/tmp/fifo --jobserver-auth=7,8"
        assert get_jobserver_config(makeflags) is None
        makeflags = " --jobserver-auth=7,8 --jobserver-auth=fifo:/tmp/fifo"
        assert get_jobserver_config(makeflags) == "/tmp/fifo"

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
            assert fcntl.fcntl(r, fcntl.F_GETFD) >= 0
            assert fcntl.fcntl(w, fcntl.F_GETFD) >= 0
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
        assert fcntl.fcntl(r, fcntl.F_GETFD) >= 0
        assert fcntl.fcntl(w, fcntl.F_GETFD) >= 0
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
        js = PosixJobServer(4, makeflags="")

        try:
            assert js.created is True
            assert js.fifo_path is not None
            assert os.path.exists(js.fifo_path)
            assert js.tokens_acquired == 0
            assert fcntl.fcntl(js.r, fcntl.F_GETFD) >= 0
            assert fcntl.fcntl(js.w, fcntl.F_GETFD) >= 0
        finally:
            js.close()

    def test_attaches_to_existing_fifo(self):
        """Should attach to existing FIFO jobserver from environment."""
        js1 = PosixJobServer(4, makeflags="")
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

    def test_setup_attaches_to_fifo_from_makeflags(self):
        """A FIFO jobserver advertised in MAKEFLAGS is attached to instead of creating one."""
        js1 = PosixJobServer(4, makeflags="")
        assert js1.fifo_path
        js2 = PosixJobServer(4, makeflags=f" -j4 --jobserver-auth=fifo:{js1.fifo_path}")
        try:
            assert js2.created is False
            assert js2.fifo_path == js1.fifo_path
            # The creator's tokens are visible through the attached file descriptors.
            assert js2.acquire(1) == 1
            js2.release()
        finally:
            js2.close()
            js1.close()

    def test_setup_ignores_pipe_from_makeflags(self):
        """Spack does not attach to an old pipe jobserver advertised in MAKEFLAGS."""
        r, w = os.pipe()
        try:
            js = PosixJobServer(4, makeflags=f" -j4 --jobserver-auth={r},{w}")
            try:
                assert js.created is True
                assert js.fifo_path is not None
                assert (js.r, js.w) != (r, w)
            finally:
                js.close()
        finally:
            os.close(r)
            os.close(w)

    def test_update_selector_registers_and_unregisters(self):
        """update_selector idempotently (un)registers the token fd based on the wake flag."""
        js = PosixJobServer(2, makeflags="")
        selector = selectors.DefaultSelector()
        try:
            js.update_selector(selector, wake=True)
            assert js.r in selector.get_map()
            js.update_selector(selector, wake=True)  # already registered: no-op
            assert len(selector.get_map()) == 1
            js.update_selector(selector, wake=False)
            assert js.r not in selector.get_map()
            js.update_selector(selector, wake=False)  # already unregistered: no-op
        finally:
            selector.close()
            js.close()

    def test_acquire_tokens(self):
        """Should acquire tokens from jobserver."""
        js = PosixJobServer(5, makeflags="")

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
        js = PosixJobServer(5, makeflags="")

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
        js = PosixJobServer(4, makeflags="")

        try:
            assert js.tokens_acquired == 0
            js.release()
            assert js.tokens_acquired == 0
        finally:
            js.close()

    def test_makeflags_fifo_gmake_44(self):
        """Should use fifo style for gmake >= 4.4."""
        js = PosixJobServer(8, makeflags="")

        try:
            makeflags = js.makeflags(Spec("gmake@=4.4"))
            assert isinstance(makeflags, FifoMakeflags)
            assert (makeflags.fifo_path, makeflags.num_jobs) == (js.fifo_path, 8)
        finally:
            js.close()

    def test_makeflags_pipe_gmake_40(self):
        """Should use pipe style for gmake 4.0-4.3."""
        js = PosixJobServer(8, makeflags="")

        try:
            makeflags = js.makeflags(Spec("gmake@=4.0"))
            assert isinstance(makeflags, PipeMakeflags)
            assert (makeflags.fifo_path, makeflags.flag) == (js.fifo_path, "--jobserver-auth")
        finally:
            js.close()

    def test_makeflags_pipe_old_flag_gmake_3(self):
        """Should use pipe style with the old --jobserver-fds flag name for gmake < 4.0."""
        js = PosixJobServer(8, makeflags="")

        try:
            makeflags = js.makeflags(Spec("gmake@=3.9"))
            assert isinstance(makeflags, PipeMakeflags)
            assert (makeflags.fifo_path, makeflags.flag) == (js.fifo_path, "--jobserver-fds")
        finally:
            js.close()

    def test_makeflags_no_gmake(self):
        """Should use fifo style when there is no gmake (modern default)."""
        js = PosixJobServer(6, makeflags="")

        try:
            makeflags = js.makeflags(None)
            assert isinstance(makeflags, FifoMakeflags)
            assert (makeflags.fifo_path, makeflags.num_jobs) == (js.fifo_path, 6)
        finally:
            js.close()

    def test_close_removes_created_fifo(self):
        """Should remove FIFO and directory if created by this instance."""
        js = PosixJobServer(4, makeflags="")
        fifo_path = js.fifo_path
        assert fifo_path and os.path.exists(fifo_path)
        js.close()
        assert not os.path.exists(os.path.dirname(fifo_path))

    def test_close_warns_when_spack_holds_tokens(self):
        """Should warn when Spack closes the jobserver while still holding acquired tokens."""
        js = PosixJobServer(4, makeflags="")
        js.acquire(1)  # Spack acquires a token without releasing it
        with pytest.warns(UserWarning, match="Spack failed to release jobserver tokens"):
            js.close()

    def test_close_warns_when_subprocess_holds_tokens(self):
        """Should warn when a subprocess acquired a token but never released it."""
        js1 = PosixJobServer(4, makeflags="")
        os.read(js1.r, 1)  # A subprocess acquires a token without releasing it
        with pytest.warns(UserWarning, match="1 jobserver token was not released"):
            js1.close()

        js2 = PosixJobServer(4, makeflags="")
        os.read(js2.r, 2)  # A subprocess acquires two tokens without releasing them
        with pytest.warns(UserWarning, match="2 jobserver tokens were not released"):
            js2.close()

    def test_has_target_parallelism(self):
        """has_target_parallelism() should be True initially."""
        js = PosixJobServer(4, makeflags="")
        try:
            assert js.has_target_parallelism() is True
            js.target_jobs = js.num_jobs - 1
            assert js.has_target_parallelism() is False
        finally:
            js.close()

    def test_increase_parallelism_not_created(self):
        """increase_parallelism() should be a no-op when not self.created."""
        # Simulate an externally attached jobserver by patching created after construction.
        js = PosixJobServer(3, makeflags="")
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
        js = PosixJobServer(3, makeflags="")
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
        js = PosixJobServer(1, makeflags="")
        try:
            # target_jobs starts at 1
            assert js.target_jobs == 1
            js.decrease_parallelism()
            assert js.target_jobs == 1
        finally:
            js.close()

    def test_decrease_parallelism_token_available(self):
        """When pipe has tokens, decrease_parallelism discards one immediately."""
        js = PosixJobServer(3, makeflags="")
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
        js = PosixJobServer(3, makeflags="")
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
        js = PosixJobServer(3, makeflags="")
        try:
            original_num = js.num_jobs
            js.maybe_discard_tokens()  # to_discard == 0
            assert js.num_jobs == original_num
        finally:
            js.close()

    def test_maybe_discard_tokens_discards_when_available(self):
        """maybe_discard_tokens() should consume tokens from the pipe."""
        js = PosixJobServer(4, makeflags="")
        try:
            # Manually set target lower to create a discard requirement.
            js.target_jobs = js.num_jobs - 2
            original_num = js.num_jobs
            js.maybe_discard_tokens()
            assert js.num_jobs < original_num
        finally:
            js.close()

    def test_maybe_discard_tokens_noop_on_blocking(self):
        """maybe_discard_tokens() should not raise when pipe is empty."""
        js = PosixJobServer(3, makeflags="")
        try:
            # Drain all tokens from the pipe (simulates subprocesses holding them).
            assert js.acquire(ALL_TOKENS) == js.num_jobs - 1
            original_num = js.num_jobs
            # Artificially lower target so a discard is requested, but pipe is empty.
            js.target_jobs = js.num_jobs - 1
            js.maybe_discard_tokens()  # Should not raise; num_jobs unchanged.
            assert js.num_jobs == original_num
        finally:
            js.close()

    def test_release_discards_token_when_target_below_num(self):
        """release() should discard a token (not return it) when target_jobs < num_jobs."""
        js = PosixJobServer(4, makeflags="")
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


def parse_pipe_fds(makeflags: str):
    """Return the (r, w) pair advertised in a pipe style MAKEFLAGS value."""
    r, w = makeflags.rsplit("=", 1)[1].split(",")
    return int(r), int(w)


class TestApplyMakeflags:
    """Test applying MAKEFLAGS to an environment, which happens in the build child process."""

    def test_fifo_style(self):
        """Fifo style points gmake at the FIFO by path."""
        env = {}
        FifoMakeflags("/tmp/x", 4).apply(env)
        assert env["MAKEFLAGS"] == " -j4 --jobserver-auth=fifo:/tmp/x"

    def test_no_makeflags(self):
        """No jobserver: nothing to set."""
        env = {}
        NoMakeflags().apply(env)
        assert env == {}

    def test_pipe_style_uses_fresh_blocking_fds(self):
        """Pipe style should make the build process open its own fds, distinct from Spack's, and
        end up blocking rather than inheriting Spack's non-blocking read fd."""
        js = PosixJobServer(4, makeflags="")
        try:
            env = {}
            PipeMakeflags(js.fifo_path, "--jobserver-auth").apply(env)
            # The -j flag has no number: a number makes old gmake ignore the jobserver.
            assert env["MAKEFLAGS"].startswith(" -j --jobserver-auth=")
            r, w = parse_pipe_fds(env["MAKEFLAGS"])
            try:
                assert (r, w) != (js.r, js.w)
                assert not (fcntl.fcntl(r, fcntl.F_GETFL) & os.O_NONBLOCK)
                os.write(js.w, b"+")
                assert os.read(r, 1) == b"+"
            finally:
                os.close(r)
                os.close(w)
        finally:
            js.close()
