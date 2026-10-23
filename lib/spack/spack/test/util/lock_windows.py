# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the ctypes-based Windows locking internals in spack.util.lock_windows.

``LockFileEx`` locks belong to the handle that took them, so a second, independently opened
handle on the same file behaves exactly like another process. Several tests below use one to
stand in for a competing process.
"""

import os
import pathlib
import sys
from contextlib import contextmanager

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

import ctypes
import msvcrt

import spack.util.lock as lk
import spack.util.lock_windows as lkw

WHOLE = (0, lkw.GATE_OFFSET)


@contextmanager
def other_process(path: str):
    """A handle on ``path`` that is independent of the lock tracker, i.e. another "process"."""
    fd = os.open(path, os.O_RDWR | os.O_CREAT)
    try:
        yield msvcrt.get_osfhandle(fd)
    finally:
        os.close(fd)


def try_lock(handle, flags, start, length) -> bool:
    low, high = lkw._low_high(length)
    overlapped = lkw._setup_overlapped(start)
    return lkw._win_lock_file_ex(handle, flags | lkw.LockType.LOCK_NB, low, high, overlapped)


def unlock(handle, start, length) -> None:
    low, high = lkw._low_high(length)
    lkw._win_unlock_file_ex(handle, low, high, lkw._setup_overlapped(start))


def gate(start, length):
    return lkw.GATE_OFFSET + start, length


@pytest.fixture
def lock_path(tmp_path: pathlib.Path):
    return str(tmp_path / "lockfile")


@pytest.mark.parametrize("winerror", [32, 33])  # ERROR_SHARING_VIOLATION, ERROR_LOCK_VIOLATION
def test_poll_lock_contended_win(lock_path, monkeypatch, winerror):
    """A LockFileEx failure with ERROR_SHARING_VIOLATION/ERROR_LOCK_VIOLATION means someone else
    holds the lock: poll() should report that as a failed (non-blocking) attempt, not raise."""

    def fake_lock_file_ex(handle, flags, reserved, low, high, overlapped):
        ctypes.set_last_error(winerror)
        return 0

    lock = lk.Lock(lock_path)
    lock.backend.prepare(lk.LockType.READ)
    monkeypatch.setattr(lkw._kernel32, "LockFileEx", fake_lock_file_ex)
    assert not lock.backend.poll(lk.LockType.READ)
    # the handle is not kept open between attempts
    assert lock.backend._file_ref is None


def test_poll_lock_unexpected_error_win(lock_path, monkeypatch):
    """A LockFileEx failure with any winerror other than ERROR_SHARING_VIOLATION/
    ERROR_LOCK_VIOLATION is a real error, and should propagate as an OSError."""

    def fake_lock_file_ex(handle, flags, reserved, low, high, overlapped):
        ctypes.set_last_error(5)  # ERROR_ACCESS_DENIED: not a contention code
        return 0

    lock = lk.Lock(lock_path)
    lock.backend.prepare(lk.LockType.READ)
    monkeypatch.setattr(lkw._kernel32, "LockFileEx", fake_lock_file_ex)
    with pytest.raises(OSError):
        lock.backend.poll(lk.LockType.READ)


def test_whole_file_range():
    """A zero length covers everything from start up to the gates."""
    assert lk.Lock("lockfile").backend._length == lkw.GATE_OFFSET
    assert lk.Lock("lockfile", start=2**62).backend._length == lkw.GATE_OFFSET - 2**62
    # the largest range used by spack's prefix locks
    lk.Lock("lockfile", start=lkw.GATE_OFFSET - 1, length=1)
    with pytest.raises(ValueError):
        lk.Lock("lockfile", start=lkw.GATE_OFFSET, length=1)


def test_whole_file_lock_covers_high_offsets(lock_path):
    """Whole-file locks must conflict with byte-range locks at any offset spack uses."""
    lock = lk.Lock(lock_path)
    lock.acquire_write()
    try:
        with other_process(lock_path) as h:
            assert not try_lock(h, lkw.LockType.LOCK_SH, 2**62, 1)
    finally:
        lock.release_write()


def test_failed_attempt_releases_handle(lock_path):
    """A failed attempt must not keep the file open, or other processes can't delete it."""
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        lock = lk.Lock(lock_path)
        assert not lock.try_acquire_read()
        assert lock.backend._file_ref is None
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(timeout=0.05)
        assert lock.backend._file_ref is None
        unlock(h, *WHOLE)

    with lk.ReadTransaction(lock):
        pass
    os.unlink(lock_path)


def test_fresh_write_takes_the_gate(lock_path):
    """Every write acquisition goes through the gate, so a writer can't slip into the window in
    which an upgrade has dropped its read lock."""
    lock = lk.Lock(lock_path)
    with lk.ReadTransaction(lock):
        pass
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *gate(*WHOLE))  # an upgrade is in progress
        assert not lock.try_acquire_write()
        unlock(h, *gate(*WHOLE))
    assert lock.try_acquire_write()
    lock.release_write()


def test_upgrade_excludes_writers_while_read_is_dropped(lock_path, monkeypatch):
    """While an upgrade has briefly dropped its read lock, a writer following the gate protocol
    can't take the range."""
    lock = lk.Lock(lock_path)
    lock.acquire_read()
    attempts = []

    with other_process(lock_path) as h:
        real_unlock = lkw._win_unlock_file_ex

        def unlock_and_race(*args):
            real_unlock(*args)
            if not attempts:  # right after the read lock is dropped
                attempts.append(try_lock(h, lkw.LockType.LOCK_EX, *gate(*WHOLE)))

        monkeypatch.setattr(lkw, "_win_unlock_file_ex", unlock_and_race)
        lock.acquire_write()
        monkeypatch.undo()

        assert attempts == [False]
        assert not try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)

    lock.release_write()
    lock.release_read()


def test_failed_upgrade_keeps_read_lock(lock_path):
    """If another reader prevents an upgrade, the original read lock must still be held."""
    lock = lk.Lock(lock_path)
    lock.acquire_read()
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
        assert not lock.try_acquire_write()
        assert lock._reads == 1 and lock._writes == 0
        unlock(h, *WHOLE)
        # we still hold the shared lock, so no writer can get in
        assert not try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
    lock.release_read()
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_upgrade_does_not_leave_files_behind(tmp_path: pathlib.Path):
    lock = lk.Lock(str(tmp_path / "lockfile"))
    lock.acquire_read()
    lock.acquire_write()
    lock.release_write()
    lock.release_read()
    assert os.listdir(tmp_path) == ["lockfile"]


def test_downgrade_never_unlocks(lock_path, monkeypatch):
    """Downgrading must keep the range locked throughout (no window for another writer)."""
    lock = lk.Lock(lock_path)
    lock.acquire_write()
    with other_process(lock_path) as h:
        real_unlock = lkw._win_unlock_file_ex
        results = []

        def unlock_and_race(*args):
            real_unlock(*args)
            results.append(try_lock(h, lkw.LockType.LOCK_EX, *WHOLE))

        monkeypatch.setattr(lkw, "_win_unlock_file_ex", unlock_and_race)
        lock.downgrade_write_to_read()
        monkeypatch.undo()

        assert results == [False]
        # now shared: other readers are allowed
        assert try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
        unlock(h, *WHOLE)
    lock.release_read()


def test_same_process_locks_on_different_ranges(lock_path):
    """Locks on different ranges of one file, in one process, are tracked independently."""
    whole = lk.Lock(lock_path)
    byte = lk.Lock(lock_path, start=5, length=1)
    whole.acquire_read()
    byte.acquire_read()
    assert whole.backend._lock_group is not byte.backend._lock_group
    whole.release_read()
    byte.release_read()
    assert not lkw.WINDOWS_RANGE_LOCK_TRACKER._groups


def test_same_process_locks_share_range(lock_path):
    """A second Lock on the same range shares the real lock instead of contending with it."""
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_write()
    assert b.try_acquire_read()
    assert a.backend._lock_group is b.backend._lock_group
    b.release_read()
    a.release_write()
    assert not lkw.WINDOWS_RANGE_LOCK_TRACKER._groups


def test_same_process_write_not_demoted_by_other_lock(lock_path):
    """One Lock releasing its write must not downgrade another Lock's write on the same range."""
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_write()
    b.acquire_read()
    b.acquire_write()
    b.release_write()  # b goes back to read, a still writes

    with other_process(lock_path) as h:
        assert not try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
        b.release_read()
        assert not try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
        a.release_write()
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_last_writer_release_downgrades_shared_range(lock_path):
    """When the last writer on a shared range releases, remaining readers keep a read lock."""
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_read()
    b.acquire_write()  # upgrades the shared range
    b.release_write()
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
        unlock(h, *WHOLE)
        assert not try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
    a.release_read()
