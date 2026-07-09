# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for behavior specific to ``spack.util.lock_posix.PosixBackend`` (``fcntl``-based locking)
that can't be exercised through the shared, platform-neutral tests in ``lock_backend.py``.

Run with pytest::

    pytest lib/spack/spack/test/util/lock_unix.py
"""

import errno
import multiprocessing
import pathlib
import sys

import pytest

import spack.util.lock as lk
from spack.test.util.lock_backend import (  # noqa: F401
    lock_dir,
    lock_fail_timeout,
    lock_path,
    read_only,
)
from spack.util.filesystem import getuid, touch, working_dir

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="fcntl is POSIX-only")

if sys.platform != "win32":
    import fcntl


@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_read_lock_on_read_only_lockfile(lock_dir, lock_path):
    """read-only directory, read-only lockfile."""
    touch(lock_path)
    with read_only(lock_path, lock_dir):
        lock = lk.Lock(lock_path)

        with lk.ReadTransaction(lock):
            pass

        with pytest.raises(lk.LockROFileError):
            with lk.WriteTransaction(lock):
                pass


@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_read_lock_no_lockfile(lock_dir, lock_path):
    """read-only directory, no lockfile (so can't create)."""
    with read_only(lock_dir):
        lock = lk.Lock(lock_path)

        with pytest.raises(lk.CantCreateLockError):
            with lk.ReadTransaction(lock):
                pass

        with pytest.raises(lk.CantCreateLockError):
            with lk.WriteTransaction(lock):
                pass


@pytest.mark.parametrize(
    "err_num,err_msg",
    [
        (errno.EACCES, "Fake EACCES error"),
        (errno.EAGAIN, "Fake EAGAIN error"),
        (errno.ENOENT, "Fake ENOENT error"),
    ],
)
def test_poll_lock_exception(tmp_path: pathlib.Path, monkeypatch, err_num, err_msg):
    """A ``fcntl.lockf`` failure with EACCES/EAGAIN means someone else holds the lock: poll()
    should report that as a failed (non-blocking) attempt, not raise. Any other errno is a real
    error and should propagate.
    """

    def _lockf(fd, cmd, len, start, whence):
        raise OSError(err_num, err_msg)

    with working_dir(str(tmp_path)):
        lockfile = "lockfile"
        lock = lk.Lock(lockfile)
        lock.acquire_read()

        monkeypatch.setattr(fcntl, "lockf", _lockf)

        if err_num in [errno.EAGAIN, errno.EACCES]:
            assert not lock._poll_lock(lk.LockType.LOCK_EX)
        else:
            with pytest.raises(OSError, match=err_msg):
                lock._poll_lock(lk.LockType.LOCK_EX)

        monkeypatch.undo()
        lock.release_read()


@pytest.mark.parametrize("acquire", ["acquire_write", "acquire_read"])
def test_acquire_after_fork(tmp_path: pathlib.Path, acquire: str):
    """After fork, acquire_write/read must not silently succeed due to inherited counters."""
    try:
        ctx = multiprocessing.get_context("fork")
    except ValueError:
        pytest.skip("fork start method not available on this platform")

    lockfile = str(tmp_path / "lockfile")
    lock = lk.Lock(lockfile)
    result = ctx.Queue()

    def child():
        assert lock._writes == 1  # due to forking, but POSIX lock is NOT held by this process
        try:
            if acquire == "acquire_write":
                lock.acquire_write(lock_fail_timeout)
            elif acquire == "acquire_read":
                lock.acquire_read(lock_fail_timeout)
            else:
                assert False  # should never get here
            result.put("no_error")
        except lk.LockTimeoutError:
            result.put("timed_out")

    lock.acquire_write()
    try:
        p = ctx.Process(target=child)
        p.start()
        p.join()
        assert result.get() == "timed_out"
    finally:
        lock.release_write()
