# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the ctypes-based Windows locking internals in spack.util.lock_windows.

``LockFileEx`` locks belong to the handle that took them, so a second, independently opened
handle on the same file behaves exactly like another process. Several tests below use one to
stand in for a competing process.
"""

import ctypes
import gc
import os
import pathlib
import signal
from contextlib import contextmanager

import pytest

import spack.error
import spack.util.lock as lk
from spack.util.filesystem import working_dir
from spack.util.lock_common import FILE_TRACKER, file_key

# Windows-only modules: this skips the whole file on other platforms
msvcrt = pytest.importorskip("msvcrt")
lkw = pytest.importorskip("spack.util.lock_windows")
win_acl = pytest.importorskip("spack.util.win_acl")

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


def is_gate(overlapped) -> bool:
    return overlapped.OffsetHigh >= lkw.GATE_OFFSET >> 32


def held_ranges(path: str):
    """The ranges of ``path`` this process holds locks on, according to the tracker."""
    open_file = FILE_TRACKER.get_ref_for_inode(file_key(os.stat(path), path))
    if open_file is None:
        return []
    return lkw.WINDOWS_RANGE_LOCK_TRACKER._groups.get(open_file, [])


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
    # the handle is not kept open after an error either
    assert lock.backend._file_ref is None


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
    assert not held_ranges(lock_path)


def test_same_process_locks_share_range(lock_path):
    """A second Lock on the same range shares the real lock instead of contending with it."""
    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_write()
    assert b.try_acquire_read()
    assert a.backend._lock_group is b.backend._lock_group
    b.release_read()
    a.release_write()
    assert not held_ranges(lock_path)


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


def test_failed_downgrade_changes_nothing(lock_path, monkeypatch):
    """If downgrading fails, the write lock is still held and its bookkeeping is unchanged."""
    real_lock = lkw._win_lock_file_ex

    def no_shared(handle, flags, low, high, overlapped):
        if not flags & lkw.LockType.LOCK_EX:
            return False
        return real_lock(handle, flags, low, high, overlapped)

    lock = lk.Lock(lock_path)
    lock.acquire_write()
    group = lock.backend._lock_group
    monkeypatch.setattr(lkw, "_win_lock_file_ex", no_shared)
    with pytest.raises(lk.LockError):
        lock.downgrade_write_to_read()
    monkeypatch.undo()

    assert lock._writes == 1 and lock._reads == 0
    assert lock.backend._mode == lk.LockType.WRITE
    assert group.mode == lk.LockType.WRITE and group.writers == 1 and group.refs == 1

    lock.release_write()
    assert not held_ranges(lock_path)
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_lost_read_lock_during_upgrade(lock_path, monkeypatch):
    """If the read lock can't be restored after a failed upgrade, the range is marked as lost:
    every Lock sharing it fails on its next mode change, and releasing it doesn't try to unlock
    a range that is no longer locked."""
    real_lock = lkw._win_lock_file_ex

    def only_gates(handle, flags, low, high, overlapped):
        if not is_gate(overlapped):
            return False
        return real_lock(handle, flags, low, high, overlapped)

    a = lk.Lock(lock_path)
    b = lk.Lock(lock_path)
    a.acquire_read()
    b.acquire_read()

    monkeypatch.setattr(lkw, "_win_lock_file_ex", only_gates)
    with pytest.raises(lk.LockError, match="Lost the read lock"):
        a.acquire_write()
    monkeypatch.undo()

    assert not held_ranges(lock_path)
    with pytest.raises(lk.LockError, match="was lost"):
        b.acquire_write()

    a.release_read()
    b.release_read()
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


@pytest.mark.parametrize("first,second", [((0, 0), (5, 1)), ((5, 1), (0, 0))])
def test_write_lock_on_overlapping_range_fails(lock_path, first, second):
    """A handle can't take an exclusive lock overlapping a range it holds, so instead of waiting
    on its own process forever, a write lock on an overlapping range raises."""
    held = lk.Lock(lock_path, start=first[0], length=first[1])
    other = lk.Lock(lock_path, start=second[0], length=second[1])
    held.acquire_read()

    with pytest.raises(lk.LockError, match="overlapping byte range"):
        other.acquire_write()
    assert other.backend._file_ref is None

    # reads on overlapping ranges are fine
    other.acquire_read()
    with pytest.raises(lk.LockError, match="overlapping byte range"):
        other.acquire_write()
    other.release_read()
    held.release_read()


def test_failed_gate_release_drops_range_lock(lock_path, monkeypatch):
    """If the gate can't be released after taking a fresh write lock, the write lock is dropped
    rather than held without being tracked."""
    real_unlock = lkw._win_unlock_file_ex

    def fail_on_gate(handle, low, high, overlapped):
        if is_gate(overlapped):
            raise OSError("fake UnlockFileEx failure")
        real_unlock(handle, low, high, overlapped)

    lock = lk.Lock(lock_path)
    monkeypatch.setattr(lkw, "_win_unlock_file_ex", fail_on_gate)
    with pytest.raises(OSError, match="fake"):
        lock.try_acquire_write()
    monkeypatch.undo()

    assert lock._writes == 0
    assert lock.backend._file_ref is None
    assert not held_ranges(lock_path)
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_ctrl_c_waits_until_lock_state_is_consistent(lock_path, monkeypatch):
    """Ctrl-C in the middle of an upgrade is held off until the lock and its bookkeeping are
    consistent again, so releasing afterwards works and frees the range."""
    real_unlock = lkw._win_unlock_file_ex
    interrupted = []

    def unlock_then_interrupt(*args):
        real_unlock(*args)
        if not interrupted:  # right after the read lock was dropped
            interrupted.append(True)
            signal.raise_signal(signal.SIGINT)

    lock = lk.Lock(lock_path)
    lock.acquire_read()
    monkeypatch.setattr(lkw, "_win_unlock_file_ex", unlock_then_interrupt)
    with pytest.raises(KeyboardInterrupt):
        lock.acquire_write()
    monkeypatch.undo()

    # the upgrade finished before the interrupt was raised
    assert lock.backend._mode == lk.LockType.WRITE
    lock.release_read()
    assert not held_ranges(lock_path)
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


@contextmanager
def opened_by_another_program(path: str):
    """Open ``path`` the way e.g. a virus scanner might: reading, and not sharing write access."""
    kernel32 = lkw._kernel32
    handle = kernel32.CreateFileW(
        path, lkw._GENERIC_READ, lkw._FILE_SHARE_READ, None, lkw._OPEN_EXISTING, 0, None
    )
    assert handle not in (None, lkw._INVALID_HANDLE_VALUE)
    try:
        yield
    finally:
        kernel32.CloseHandle(handle)


def test_file_in_use_by_another_program_is_not_read_only(lock_path):
    """A lock file another program has open can't be locked for now, but it must not be
    mistaken for a read-only file."""
    lock = lk.Lock(lock_path)
    with lk.ReadTransaction(lock):
        pass  # create the file

    with opened_by_another_program(lock_path):
        assert not lock.try_acquire_write()
        assert not lock.try_acquire_read()
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(timeout=0.05)
        assert lock.backend._file_ref is None

    assert lock.try_acquire_write()
    assert lock.backend._file_ref.fh.mode == "rb+"
    lock.release_write()


def test_held_lock_survives_cwd_change(tmp_path: pathlib.Path):
    """Checking the file again while a lock is held must not swap (and so close) the handle that
    holds the lock, even if a relative path now names a different file."""
    first, second = tmp_path / "first", tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (second / "lockfile").write_text("")

    with working_dir(str(first)):
        lock = lk.Lock("lockfile")
        lock.acquire_read()
    with working_dir(str(second)):
        lock.acquire_read()  # nested: re-checks the lock
        with other_process(str(first / "lockfile")) as h:
            assert not try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        lock.release_read()
        lock.release_read()
    with other_process(str(first / "lockfile")) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_debug_owner_info_is_best_effort(lock_path):
    """Windows locks are mandatory, so the owner info at the start of the file can't be read or
    written while another process locks those bytes. That must not make locking fail."""
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, 3, 1)
        lock = lk.Lock(lock_path, start=40, length=1, debug=True)
        lock.acquire_write()
        lock.release_write()
        lock.acquire_read()
        lock.release_read()
        unlock(h, 3, 1)


def test_closing_files_drops_lock_records(lock_path):
    """Closing all lock files (as the test suite does between tests) drops their OS locks, so it
    must drop their records too: a new lock on the same file has to take a real lock."""
    leaked = lk.Lock(lock_path)
    leaked.acquire_read()
    FILE_TRACKER.purge()

    lock = lk.Lock(lock_path)
    lock.acquire_read()
    assert lock.backend._lock_group is not leaked.backend._lock_group
    with other_process(lock_path) as h:
        assert not try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
    lock.release_read()

    leaked.release_read()  # its file was closed: nothing to unlock
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_dropped_lock_keeps_holding(lock_path):
    """As on POSIX, a Lock that is garbage collected while holding the lock keeps holding it."""
    lock = lk.Lock(lock_path)
    lock.acquire_write()
    del lock
    gc.collect()
    with other_process(lock_path) as h:
        assert not try_lock(h, lkw.LockType.LOCK_SH, *WHOLE)
    FILE_TRACKER.purge()


def test_write_on_held_write_range_is_not_an_overlap(lock_path):
    """Joining a write lock this process already holds needs no new OS lock, so an overlapping
    read lock on another range doesn't get in the way."""
    byte = lk.Lock(lock_path, start=5, length=1)
    whole = lk.Lock(lock_path)
    same_byte = lk.Lock(lock_path, start=5, length=1)
    byte.acquire_write()
    whole.acquire_read()
    same_byte.acquire_write()
    assert same_byte.backend._lock_group is byte.backend._lock_group
    same_byte.release_write()
    whole.release_read()
    byte.release_write()
    with other_process(lock_path) as h:
        assert try_lock(h, lkw.LockType.LOCK_EX, *WHOLE)
        unlock(h, *WHOLE)


def test_check_lock_safety(tmp_path: pathlib.Path):
    """Disabling locks is refused when users other than the owner can write to the prefix."""
    path = str(tmp_path)
    win_acl.set_exclusive_owner_control(path)
    lk.check_lock_safety(path)

    # an entry that only applies to the directory's contents doesn't make it writable
    sd = win_acl.SecurityDescriptor.from_file(path)
    sd.add_ace(
        win_acl.AccessControlEntry(
            win_acl.AceType.SDDL_ACCESS_ALLOWED,
            flags=[win_acl.AceFlags.SDDL_INHERIT_ONLY, win_acl.AceFlags.SDDL_CONTAINER_INHERIT],
            rights=win_acl.FileAccessRights.FILE_GENERIC_WRITE,
            sid="AU",
        )
    )
    sd.apply(path)
    lk.check_lock_safety(path)

    # read access for everyone is fine
    sd.add_ace(
        win_acl.AccessControlEntry(
            win_acl.AceType.SDDL_ACCESS_ALLOWED,
            rights=win_acl.FileAccessRights.FILE_GENERIC_READ,
            sid="WD",
        )
    )
    sd.apply(path)
    lk.check_lock_safety(path)

    sd.add_ace(
        win_acl.AccessControlEntry(
            win_acl.AceType.SDDL_ACCESS_ALLOWED,
            rights=win_acl.FileAccessRights.FILE_GENERIC_WRITE,
            sid="AU",
        )
    )
    sd.apply(path)
    with pytest.raises(spack.error.SpackError, match="writable by Authenticated Users"):
        lk.check_lock_safety(path)
