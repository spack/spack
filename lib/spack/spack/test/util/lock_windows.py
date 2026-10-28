# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the Windows lock backend.

``LockFileEx`` locks belong to the file handle that took them, so a second handle on the lock
file, opened with ``os.open``, stands in for another process.
"""

import ctypes
import os
import pathlib
from contextlib import contextmanager

import pytest

import spack.util.lock as lk

lkw = pytest.importorskip("spack.util.lock_windows")

WHOLE = (0, 1 << 63)


@pytest.fixture
def lock_path(tmp_path: pathlib.Path):
    return str(tmp_path / "lockfile")


@contextmanager
def other_process(path: str):
    fd = os.open(path, os.O_RDWR | os.O_CREAT)
    try:
        yield fd
    finally:
        os.close(fd)


def gate(start, length):
    return lkw.GATE_OFFSET + start, length


def test_lock_conflict(lock_path, monkeypatch):
    """ERROR_LOCK_VIOLATION means another handle holds the lock: the attempt fails, and the file
    is closed."""

    def lock_file_ex(*args):
        ctypes.set_last_error(33)
        return 0

    lock = lk.Lock(lock_path)
    monkeypatch.setattr(lkw._kernel32, "LockFileEx", lock_file_ex)
    assert not lock.try_acquire_read()
    assert lock.backend._file_ref is None


def test_lock_error(lock_path, monkeypatch):
    """Any other LockFileEx failure is an error, and the file is closed."""

    def lock_file_ex(*args):
        ctypes.set_last_error(5)  # ERROR_ACCESS_DENIED
        return 0

    lock = lk.Lock(lock_path)
    monkeypatch.setattr(lkw._kernel32, "LockFileEx", lock_file_ex)
    with pytest.raises(OSError):
        lock.try_acquire_read()
    assert lock.backend._file_ref is None


def test_lock_range():
    """A zero length locks everything up to the gates, and ranges can't reach the gates."""
    assert lk.Lock("lockfile").backend._length == lkw.GATE_OFFSET
    assert lk.Lock("lockfile", start=2**62).backend._length == lkw.GATE_OFFSET - 2**62
    lk.Lock("lockfile", start=lkw.GATE_OFFSET - 1, length=1)
    with pytest.raises(ValueError):
        lk.Lock("lockfile", start=lkw.GATE_OFFSET, length=1)


def test_whole_file_lock_covers_byte_range_locks(lock_path):
    lock = lk.Lock(lock_path)
    lock.acquire_write()
    with other_process(lock_path) as fd:
        assert not lkw._lock_file(fd, False, lkw.GATE_OFFSET - 1, 1)
    lock.release_write()


def test_file_is_closed_unless_locked(lock_path):
    """Windows can't delete open files, so the lock file is only kept open while locked."""
    lock = lk.Lock(lock_path)
    with other_process(lock_path) as fd:
        assert lkw._lock_file(fd, True, *WHOLE)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(timeout=0.05)
        assert lock.backend._file_ref is None

    with lk.WriteTransaction(lock):
        pass
    os.unlink(lock_path)


def test_write_lock_waits_for_gate(lock_path):
    """Writers take the gate first, so they can't take the range while an upgrade has briefly
    released it."""
    lock = lk.Lock(lock_path)
    with other_process(lock_path) as fd:
        assert lkw._lock_file(fd, True, *gate(*WHOLE))
        assert not lock.try_acquire_write()
        lkw._unlock_file(fd, *gate(*WHOLE))
    assert lock.try_acquire_write()
    lock.release_write()


def test_upgrade_holds_gate(lock_path, monkeypatch):
    """While an upgrade has released the range, its gate keeps writers out."""
    lock = lk.Lock(lock_path)
    lock.acquire_read()
    real_unlock_file = lkw._unlock_file
    attempts = []

    with other_process(lock_path) as fd:

        def unlock_file(lock_fd, offset, length):
            real_unlock_file(lock_fd, offset, length)
            if offset < lkw.GATE_OFFSET:  # the range was released
                attempts.append(lkw._lock_file(fd, True, *gate(*WHOLE)))

        monkeypatch.setattr(lkw, "_unlock_file", unlock_file)
        lock.acquire_write()
        monkeypatch.undo()

        assert attempts == [False]
        assert not lkw._lock_file(fd, False, *WHOLE)

    lock.release_write()
    lock.release_read()


def test_failed_upgrade_keeps_read_lock(lock_path):
    lock = lk.Lock(lock_path)
    lock.acquire_read()
    with other_process(lock_path) as fd:
        assert lkw._lock_file(fd, False, *WHOLE)
        assert not lock.try_acquire_write()
        lkw._unlock_file(fd, *WHOLE)
        assert not lkw._lock_file(fd, True, *WHOLE)
    lock.release_read()


def test_downgrade_keeps_range_locked(lock_path, monkeypatch):
    lock = lk.Lock(lock_path)
    lock.acquire_write()
    real_unlock_file = lkw._unlock_file
    attempts = []

    with other_process(lock_path) as fd:

        def unlock_file(lock_fd, offset, length):
            real_unlock_file(lock_fd, offset, length)
            attempts.append(lkw._lock_file(fd, True, *WHOLE))

        monkeypatch.setattr(lkw, "_unlock_file", unlock_file)
        lock.downgrade_write_to_read()
        monkeypatch.undo()

        assert attempts == [False]
        assert lkw._lock_file(fd, False, *WHOLE)
        lkw._unlock_file(fd, *WHOLE)
    lock.release_read()


def test_locks_in_one_process_share_a_range(lock_path):
    """Like fcntl locks, locks on the same range in one process don't conflict."""
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_write()
    assert b.try_acquire_read()
    assert b.try_acquire_write()
    b.release_write()
    b.release_read()

    with other_process(lock_path) as fd:
        assert not lkw._lock_file(fd, False, *WHOLE)
        a.release_write()
        assert lkw._lock_file(fd, True, *WHOLE)
        lkw._unlock_file(fd, *WHOLE)


def test_shared_range_stays_exclusive_until_last_writer(lock_path):
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_write()
    b.acquire_read()
    b.acquire_write()
    b.release_write()  # a still writes

    with other_process(lock_path) as fd:
        assert not lkw._lock_file(fd, False, *WHOLE)
        a.release_write()  # b still reads
        assert lkw._lock_file(fd, False, *WHOLE)
        lkw._unlock_file(fd, *WHOLE)
        assert not lkw._lock_file(fd, True, *WHOLE)
    b.release_read()


def test_locks_on_other_ranges_are_separate(lock_path):
    whole = lk.Lock(lock_path)
    byte = lk.Lock(lock_path, start=5, length=1)
    whole.acquire_read()
    byte.acquire_read()
    assert whole.backend._held is not byte.backend._held
    whole.release_read()
    byte.release_read()


def test_closed_files_lose_their_locks(lock_path):
    """Closing all lock files (as the test suite does) drops their locks, so a new lock on the
    same file must take a real lock."""
    leaked = lk.Lock(lock_path)
    leaked.acquire_read()
    lk.FILE_TRACKER.purge()

    lock = lk.Lock(lock_path)
    lock.acquire_read()
    with other_process(lock_path) as fd:
        assert not lkw._lock_file(fd, True, *WHOLE)
    lock.release_read()
