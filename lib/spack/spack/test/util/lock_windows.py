# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the ctypes-based Windows locking internals in spack.util.lock.

These exercise behavior specific to WindowsBackend's LockFileEx error handling (see
spack.util.lock._win_lock_file_ex): errors that mean "someone else holds this lock" must be
reported as a failed poll, not raised, while any other error is a real failure.
"""

import pathlib
import sys

import pytest

import spack.util.lock as lk
from spack.util.filesystem import working_dir

pytestmark = pytest.mark.skipif(
    sys.platform != "win32", reason="ctypes kernel32 bindings are Windows-only"
)

if sys.platform == "win32":
    import ctypes


@pytest.mark.parametrize("winerror", [32, 33])  # ERROR_SHARING_VIOLATION, ERROR_LOCK_VIOLATION
def test_poll_lock_contended_win(tmp_path: pathlib.Path, monkeypatch, winerror):
    """A LockFileEx failure with ERROR_SHARING_VIOLATION/ERROR_LOCK_VIOLATION means someone else
    holds the lock: poll() should report that as a failed (non-blocking) attempt, not raise."""

    def fake_lock_file_ex(handle, flags, reserved, low, high, overlapped):
        ctypes.set_last_error(winerror)
        return 0

    with working_dir(str(tmp_path)):
        lock = lk.Lock("lockfile")
        lock.acquire_read()

        monkeypatch.setattr(lk._kernel32, "LockFileEx", fake_lock_file_ex)
        assert not lock._poll_lock(lk.LockType.LOCK_EX)
        monkeypatch.undo()

        lock.release_read()


def test_poll_lock_unexpected_error_win(tmp_path: pathlib.Path, monkeypatch):
    """A LockFileEx failure with any winerror other than ERROR_SHARING_VIOLATION/
    ERROR_LOCK_VIOLATION is a real error, and should propagate as an OSError."""

    def fake_lock_file_ex(handle, flags, reserved, low, high, overlapped):
        ctypes.set_last_error(5)  # ERROR_ACCESS_DENIED: not a contention code
        return 0

    with working_dir(str(tmp_path)):
        lock = lk.Lock("lockfile")
        lock.acquire_read()

        monkeypatch.setattr(lk._kernel32, "LockFileEx", fake_lock_file_ex)
        with pytest.raises(OSError):
            lock._poll_lock(lk.LockType.LOCK_EX)
        monkeypatch.undo()

        lock.release_read()
