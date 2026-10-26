# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LockFileEx-based lock backend for Windows, and the ctypes kernel32 bindings it needs."""

import sys

if sys.platform != "win32":
    # Also lets mypy skip this module when run on other platforms.
    raise ImportError("spack.util.lock_windows can only be imported on Windows")

import ctypes
import msvcrt
from ctypes import wintypes
from typing import Dict, List, Optional, Tuple

from spack.util import tty
from spack.util.lock_common import FILE_TRACKER, DevIno, GenericLockBackend, LockError
from spack.util.lock_common import LockType as _LockType


class LockType(_LockType):
    # From the Windows SDK (winbase.h): not exposed by ctypes, so hardcoded here.
    LOCK_SH = 0  # shared lock is the default (absence of the exclusive flag)
    LOCK_EX = 0x00000002  # LOCKFILE_EXCLUSIVE_LOCK
    LOCK_NB = 0x00000001  # LOCKFILE_FAIL_IMMEDIATELY


class _OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_void_p),
        ("InternalHigh", ctypes.c_void_p),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", wintypes.HANDLE),
    ]


_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_kernel32.LockFileEx.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.POINTER(_OVERLAPPED),
]
_kernel32.LockFileEx.restype = wintypes.BOOL

_kernel32.UnlockFileEx.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.POINTER(_OVERLAPPED),
]
_kernel32.UnlockFileEx.restype = wintypes.BOOL

# winerror 32: "The process cannot access the file because it is being used by another
#     process."
# winerror 33: "The process cannot access the file because another process has locked a
#     portion of the file."
_ERROR_SHARING_VIOLATION = 32
_ERROR_LOCK_VIOLATION = 33


def _low_high(value):
    low = value & 0xFFFFFFFF
    high = (value >> 32) & 0xFFFFFFFF
    return low, high


def _setup_overlapped(offset):
    overlapped = _OVERLAPPED()
    # hEvent needs to be null per LockFileEx/UnlockFileEx docs
    overlapped.hEvent = 0
    overlapped.Offset, overlapped.OffsetHigh = _low_high(offset)
    return overlapped


def _win_handle(fd: int) -> int:
    """The raw Win32 HANDLE backing a Python file descriptor."""
    return msvcrt.get_osfhandle(fd)


def _win_lock_file_ex(handle: int, flags: int, low: int, high: int, overlapped) -> bool:
    """Wraps ``LockFileEx``. Returns whether the lock was acquired: True on success, False if
    the range is already locked by someone else (only possible when ``flags`` includes
    ``LockType.LOCK_NB``). Raises ``OSError`` for any other failure.
    """
    if _kernel32.LockFileEx(handle, flags, 0, low, high, ctypes.byref(overlapped)):
        return True
    err = ctypes.get_last_error()
    if err in (_ERROR_SHARING_VIOLATION, _ERROR_LOCK_VIOLATION):
        return False
    raise ctypes.WinError(err)


def _win_unlock_file_ex(handle: int, low: int, high: int, overlapped) -> None:
    """Wraps ``UnlockFileEx``. Raises ``OSError`` on failure."""
    if not _kernel32.UnlockFileEx(handle, 0, low, high, ctypes.byref(overlapped)):
        raise ctypes.WinError(ctypes.get_last_error())


#: Spack lock ranges must lie in ``[0, GATE_OFFSET)``. The upgrade "gate" for the range
#: ``[start, start + length)`` is ``[GATE_OFFSET + start, GATE_OFFSET + start + length)`` of the
#: same file, so the gates of two ranges overlap exactly when the ranges themselves do, and no
#: extra file is needed (Windows allows locking byte ranges beyond the end of a file).
GATE_OFFSET = 1 << 63


class WindowsRangeLock:
    """The one real ``LockFileEx`` lock this process holds on a given byte range, shared by every
    ``WindowsBackend`` for that exact range. See ``WindowsRangeLockTracker``.
    """

    __slots__ = ("start", "length", "mode", "refs", "writers", "lost")

    def __init__(self, start: int, length: int, mode: int):
        self.start = start
        self.length = length
        #: LockType.READ or LockType.WRITE: the mode of the real OS lock currently held
        self.mode = mode
        #: number of backends attached to this lock
        self.refs = 1
        #: number of attached backends that hold it in WRITE mode
        self.writers = 1 if mode == LockType.WRITE else 0
        #: True if the real OS lock was lost (see ``WindowsBackend._upgrade_to_write``)
        self.lost = False


class WindowsRangeLockTracker:
    """Tracks byte ranges the current process holds real Windows locks on, so that a second
    ``Lock`` in the same process requesting the same range shares the *same* real lock state
    instead of contending with its own process.

    Windows ``LockFileEx`` locks are scoped to the specific *handle* that acquired them, and a
    handle cannot take an exclusive lock on a range that is already locked, even by itself.
    Spack's locking code (e.g. ``FailureTracker``/``SpecLocker`` re-checking a lock it itself
    holds via a second, independent ``Lock`` object, or a plain upgrade/downgrade) would
    otherwise contend with itself.

    Every ``WindowsBackend`` for a given file shares the same open handle (via ``FILE_TRACKER``),
    and this tracker records the one real lock ``mode`` held on a range, with reference and
    writer counts, so the lock state for a range can be updated without contention.

    Only identical ranges are shared: as with ``fcntl`` (see ``Lock``), a process must not hold
    locks on overlapping but different byte ranges of the same file.
    """

    def __init__(self):
        self._groups: Dict[DevIno, List[WindowsRangeLock]] = {}

    def find(self, key: DevIno, start: int, length: int) -> Optional[WindowsRangeLock]:
        """Return the lock this process holds on exactly [start, start+length), if any."""
        for group in self._groups.get(key, []):
            if group.start == start and group.length == length:
                return group
        return None

    def overlaps(self, key: DevIno, start: int, length: int) -> bool:
        """Whether this process holds a lock on a range that overlaps, but is not identical to,
        [start, start+length)."""
        return any(
            group.start < start + length
            and start < group.start + group.length
            and (group.start, group.length) != (start, length)
            for group in self._groups.get(key, [])
        )

    def register(self, key: DevIno, group: WindowsRangeLock) -> None:
        """Record a freshly, really-acquired OS lock as a new group of one."""
        self._groups.setdefault(key, []).append(group)

    def forget(self, key: DevIno, group: WindowsRangeLock) -> None:
        """Drop a group that no backend references anymore."""
        groups = self._groups.get(key, [])
        if group in groups:
            groups.remove(group)
        if not groups:
            self._groups.pop(key, None)


#: Tracks real Windows byte-range locks held by this process, to make same-process,
#: cross-handle lock requests behave like POSIX fcntl.
WINDOWS_RANGE_LOCK_TRACKER = WindowsRangeLockTracker()


class WindowsBackend(GenericLockBackend):
    """LockFileEx-based lock backend for Windows.

    Like ``PosixBackend``, every ``WindowsBackend`` for a given file shares one open handle via
    the process-wide ``FILE_TRACKER`` (see ``GenericLockBackend._ensure_valid_handle``). Unlike
    ``fcntl``, ``LockFileEx``/``UnlockFileEx`` calls apply to whichever handle makes them, so
    unrelated ``Lock`` objects sharing a handle would compete for the "same" lock.
    ``WINDOWS_RANGE_LOCK_TRACKER`` tracks the locks themselves (mode, references and writers) so
    that multiple lock requests from the same process on the same range behave like POSIX locks.

    ``LockFileEx`` also cannot convert a held lock between shared and exclusive in place.
    ``poll()`` handles mode transitions internally: downgrading stacks a shared lock on the
    exclusive one before removing it (see ``_downgrade_to_read``), and upgrading briefly releases
    the range behind a "gate" lock that every writer must take first (see ``_upgrade_to_write``).

    A zero ``length`` means "to the end of the file" on POSIX; here it means everything from
    ``start`` up to ``GATE_OFFSET``.

    The file handle is released whenever the lock is released or an attempt to acquire it fails,
    since an open handle prevents other processes from deleting the file (WinError 32).
    """

    def __init__(self, path: str, start: int, length: int, debug: bool = False) -> None:
        length = length or GATE_OFFSET - start
        if start < 0 or length <= 0 or start + length > GATE_OFFSET:
            raise ValueError(
                f"lock range [{start}:{start + length}] of {path} must lie within "
                f"[0:{GATE_OFFSET}]"
            )
        super().__init__(path, start, length, debug=debug)
        #: the WindowsRangeLock this backend is attached to while it holds a lock, else None
        self._lock_group: Optional[WindowsRangeLock] = None
        #: the mode (LockType.READ or LockType.WRITE) this backend holds while attached
        self._mode: Optional[int] = None

    def __getstate__(self):
        state = super().__getstate__()
        del state["_lock_group"]
        del state["_mode"]
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._lock_group = None
        self._mode = None

    def __del__(self) -> None:
        # Guard against a Lock being dropped without an explicit release: release properly
        # (respecting shared-group bookkeeping) so a later unlink doesn't fail with WinError 32,
        # and so we don't leave a WindowsRangeLock permanently over-referenced.
        try:
            self.release()
        except Exception:
            pass

    def prepare(self, op: int) -> None:
        try:
            super().prepare(op)
        except BaseException:
            if self._lock_group is None:
                self._release_handle()
            raise

    def poll(self, op: int) -> bool:
        """Attempt to acquire the lock in ``op`` mode in a non-blocking manner. Return whether
        the attempt succeeds.
        """
        if self._lock_group is not None:
            return self._change_mode(op)

        try:
            if self._file_ref is None:  # released after a previous failed attempt
                self.prepare(op)
            acquired = self._attach_or_acquire(op)
        except BaseException:
            self._release_handle()
            raise

        if not acquired:
            self._release_handle()
        return acquired

    def _attach_or_acquire(self, op: int) -> bool:
        """Attach to the lock this process already holds on this range, or take a new one."""
        assert self._file_ref is not None
        key = self._file_ref.key
        if op == LockType.WRITE:
            self._check_no_overlap()

        group = WINDOWS_RANGE_LOCK_TRACKER.find(key, self._start, self._length)
        if group is None:
            return self._acquire_new(key, op)

        if op == LockType.WRITE and group.mode == LockType.READ:
            if not self._upgrade_to_write(group):
                return False
        group.refs += 1
        if op == LockType.WRITE:
            group.writers += 1
        self._lock_group = group
        self._mode = op
        return True

    def _check_no_overlap(self) -> None:
        """A handle can't take an exclusive lock overlapping a range it already holds, so such a
        request would wait on its own process forever: fail clearly instead."""
        assert self._file_ref is not None
        if WINDOWS_RANGE_LOCK_TRACKER.overlaps(self._file_ref.key, self._start, self._length):
            raise LockError(
                f"Cannot write lock {self.path}[{self._start}:{self._start + self._length}]: "
                "this process holds a lock on an overlapping byte range of the same file"
            )

    def _change_mode(self, op: int) -> bool:
        """Switch the mode this (attached) backend holds its range's lock in."""
        group = self._lock_group
        assert group is not None
        if group.lost:
            raise LockError(f"The lock on {self.path} was lost")
        if op == self._mode:
            return True

        if op == LockType.READ:
            if group.writers == 1:
                self._downgrade_to_read(group)
            group.writers -= 1
            self._mode = op
            return True

        self._check_no_overlap()
        if group.mode == LockType.READ and not self._upgrade_to_write(group):
            return False
        group.writers += 1
        self._mode = op
        return True

    def _acquire_new(self, key: DevIno, op: int) -> bool:
        """Non-blocking attempt to take a fresh real OS lock on this range: no backend in this
        process currently holds it.
        """
        if op == LockType.WRITE:
            if not self._lock_range(LockType.LOCK_EX, gate=True):
                return False
            acquired = False
            try:
                acquired = self._lock_range(LockType.LOCK_EX)
            finally:
                try:
                    self._unlock_range(gate=True)
                except BaseException:
                    if acquired:
                        self._unlock_range()
                    raise
        else:
            acquired = self._lock_range(LockType.LOCK_SH)

        if not acquired:
            return False

        try:
            # help for debugging distributed locking
            if self.debug:
                # All locks read the owner PID and host
                self._read_log_debug_data()
                tty.debug(
                    "{0} locked {1} [{2}:{3}] (owner={4})".format(
                        LockType.to_str(op), self.path, self._start, self._length, self.pid
                    ),
                    level=2,
                )

                # Exclusive locks write their PID/host
                if op == LockType.WRITE:
                    self._write_log_debug_data()
        except BaseException:
            self._unlock_range()
            raise

        self._lock_group = WindowsRangeLock(self._start, self._length, op)
        self._mode = op
        WINDOWS_RANGE_LOCK_TRACKER.register(key, self._lock_group)
        return True

    def _upgrade_to_write(self, group: WindowsRangeLock) -> bool:
        """Single non-blocking attempt to upgrade this range's currently-held real read lock to
        a write lock.

        ``LockFileEx`` has no atomic convert, so the read lock has to be dropped before the
        write lock can be taken. To make sure no other writer can take the range in between,
        every write acquisition (fresh or upgrade) first takes this range's gate. While we hold
        the gate only readers can take the range, so if the write lock fails our read lock can
        always be restored. Should that still fail, the range is marked as lost: every backend
        sharing it raises on its next mode change, and nothing tries to unlock it.
        """
        assert group.mode == LockType.READ
        if not self._lock_range(LockType.LOCK_EX, gate=True):
            return False

        try:
            self._unlock_range()
            try:
                if self._lock_range(LockType.LOCK_EX):
                    group.mode = LockType.WRITE
                    return True
                # Another reader holds the range: restore our read lock.
                restored = self._lock_range(LockType.LOCK_SH)
            except BaseException:
                self._lose(group)
                raise
            if not restored:
                self._lose(group)
                raise LockError(f"Lost the read lock on {self.path} while upgrading it")
            return False
        finally:
            self._unlock_range(gate=True)

    def _lose(self, group: WindowsRangeLock) -> None:
        """Record that this process no longer holds any OS lock on the group's range."""
        assert self._file_ref is not None
        group.lost = True
        WINDOWS_RANGE_LOCK_TRACKER.forget(self._file_ref.key, group)

    def _downgrade_to_read(self, group: WindowsRangeLock) -> None:
        """Convert this range's held real exclusive lock to a shared lock without ever releasing
        it.

        A handle may stack a shared lock on a range it holds exclusively, and when the same range
        is locked both ways, the first unlock removes the exclusive lock. So take the shared lock
        (granted immediately, as this handle owns the range) and unlock once.
        """
        assert group.mode == LockType.WRITE
        if not self._lock_range(LockType.LOCK_SH):
            raise LockError(f"Could not downgrade the write lock on {self.path}")
        self._unlock_range()
        group.mode = LockType.READ

    def release(self) -> None:
        """Release this backend's interest in the lock, and its ``FILE_TRACKER`` handle
        reference (closing the underlying handle once no backend uses it).

        If this was the last backend attached to this range's ``WindowsRangeLock``, performs the
        real OS-level unlock; if it was the last writer, downgrades it to a read lock. If that
        fails, the lock is still held and nothing changes.
        """
        group = self._lock_group
        if group is not None:
            assert self._file_ref is not None
            if not group.lost:
                if group.refs == 1:
                    self._unlock_range()
                    WINDOWS_RANGE_LOCK_TRACKER.forget(self._file_ref.key, group)
                elif self._mode == LockType.WRITE and group.writers == 1:
                    self._downgrade_to_read(group)
            group.refs -= 1
            if self._mode == LockType.WRITE:
                group.writers -= 1
            self._lock_group = None
            self._mode = None
        self._release_handle()

    def _release_handle(self) -> None:
        if self._file_ref is not None:
            FILE_TRACKER.release(self._file_ref)
        self._file_ref = None
        self._cached_key = None

    def _handle(self) -> int:
        assert self._file_ref is not None, "cannot lock without the file being set"
        return _win_handle(self._file_ref.fh.fileno())

    def _range(self, gate: bool) -> Tuple[_OVERLAPPED, int, int]:
        offset = self._start + (GATE_OFFSET if gate else 0)
        low, high = _low_high(self._length)
        return _setup_overlapped(offset), low, high

    def _lock_range(self, flags: int, gate: bool = False) -> bool:
        """Non-blocking ``LockFileEx`` on this range (or its gate). Returns whether it was
        acquired.
        """
        overlapped, low, high = self._range(gate)
        return _win_lock_file_ex(self._handle(), flags | LockType.LOCK_NB, low, high, overlapped)

    def _unlock_range(self, gate: bool = False) -> None:
        overlapped, low, high = self._range(gate)
        _win_unlock_file_ex(self._handle(), low, high, overlapped)
