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

from spack.new_installer import (
    JobServer,
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


class TestJobServer:
    """Test JobServer class functionality."""

    def test_creates_new_jobserver(self):
        """Should create a new FIFO-based jobserver when none exists."""
        js = JobServer(4)

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
        js1 = JobServer(4)
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
        js = JobServer(5)

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
        js = JobServer(5)

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
        js = JobServer(4)

        try:
            assert js.tokens_acquired == 0
            js.release()
            assert js.tokens_acquired == 0
        finally:
            js.close()

    def test_makeflags_fifo_gmake_44(self):
        """Should return FIFO format for gmake >= 4.4."""
        js = JobServer(8)

        try:
            flags = js.makeflags(Spec("gmake@=4.4"))
            assert flags == f" -j8 --jobserver-auth=fifo:{js.fifo_path}"
        finally:
            js.close()

    def test_makeflags_pipe_gmake_40(self):
        """Should return pipe format for gmake 4.0-4.3."""
        js = JobServer(8)

        try:
            flags = js.makeflags(Spec("gmake@=4.0"))
            assert flags == f" -j8 --jobserver-auth={js.r},{js.w}"
        finally:
            js.close()

    def test_makeflags_old_format_gmake_3(self):
        """Should return old --jobserver-fds format for gmake < 4.0."""
        js = JobServer(8)

        try:
            flags = js.makeflags(Spec("gmake@=3.9"))
            assert flags == f" -j8 --jobserver-fds={js.r},{js.w}"
        finally:
            js.close()

    def test_makeflags_no_gmake(self):
        """Should return FIFO format when no gmake (modern default)."""
        js = JobServer(6)

        try:
            flags = js.makeflags(None)
            assert flags == f" -j6 --jobserver-auth=fifo:{js.fifo_path}"
        finally:
            js.close()

    def test_close_removes_created_fifo(self):
        """Should remove FIFO and directory if created by this instance."""
        js = JobServer(4)
        fifo_path = js.fifo_path
        assert fifo_path and os.path.exists(fifo_path)
        js.close()
        assert not os.path.exists(os.path.dirname(fifo_path))

    def test_file_descriptors_are_inheritable(self):
        """Should set file descriptors as inheritable for child processes."""
        js = JobServer(4)

        try:
            assert os.get_inheritable(js.r)
            assert os.get_inheritable(js.w)
        finally:
            js.close()

    def test_connection_objects_exist(self):
        """Should create Connection objects for fd inheritance."""
        js = JobServer(4)

        try:
            assert js.r_conn is not None and js.r_conn.fileno() == js.r
            assert js.w_conn is not None and js.w_conn.fileno() == js.w
        finally:
            js.close()
