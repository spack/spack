# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Lock backend for Windows, based on ``LockFileEx``."""

import sys

if sys.platform != "win32":
    raise ImportError("spack.util.lock_windows is only available on Windows")

import ctypes
import msvcrt
from ctypes import wintypes
from typing import Dict, Optional, Tuple

from spack.util.lock import FILE_TRACKER, FileBackend, LockError, LockType, OpenFile

_LOCKFILE_FAIL_IMMEDIATELY = 0x1
_LOCKFILE_EXCLUSIVE_LOCK = 0x2
_ERROR_LOCK_VIOLATION = 33

#: Lock ranges must end at or before this offset. The range ``[start, start + length)`` has its
#: "gate" at ``[GATE_OFFSET + start, GATE_OFFSET + start + length)`` (see
#: ``WindowsBackend._upgrade``). Spack's byte-range locks use offsets of at most 63 bits.
GATE_OFFSET = 1 << 63


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


def _lock_file(fd: int, exclusive: bool, offset: int, length: int) -> bool:
    """Try once to lock a byte range of a file. Returns False if another handle holds a
    conflicting lock."""
    flags = _LOCKFILE_FAIL_IMMEDIATELY | (_LOCKFILE_EXCLUSIVE_LOCK if exclusive else 0)
    overlapped = _OVERLAPPED(Offset=offset & 0xFFFFFFFF, OffsetHigh=offset >> 32)
    handle = msvcrt.get_osfhandle(fd)
    if _kernel32.LockFileEx(
        handle, flags, 0, length & 0xFFFFFFFF, length >> 32, ctypes.byref(overlapped)
    ):
        return True
    error = ctypes.get_last_error()
    if error == _ERROR_LOCK_VIOLATION:
        return False
    raise ctypes.WinError(error)


def _unlock_file(fd: int, offset: int, length: int) -> None:
    """Unlock a byte range of a file."""
    overlapped = _OVERLAPPED(Offset=offset & 0xFFFFFFFF, OffsetHigh=offset >> 32)
    handle = msvcrt.get_osfhandle(fd)
    if not _kernel32.UnlockFileEx(
        handle, 0, length & 0xFFFFFFFF, length >> 32, ctypes.byref(overlapped)
    ):
        raise ctypes.WinError(ctypes.get_last_error())


class _RangeLock:
    """The lock this process holds on a byte range, shared by all its backends for that range."""

    __slots__ = ("refs", "writers")

    def __init__(self) -> None:
        #: number of backends holding the lock
        self.refs = 0
        #: number of backends holding it for writing; the OS lock is exclusive if this is > 0
        self.writers = 0


#: The locks this process holds, by the file they were taken through and their range.
_held_locks: Dict[Tuple[OpenFile, int, int], _RangeLock] = {}


class WindowsBackend(FileBackend):
    """``LockFileEx``-based lock backend.

    ``LockFileEx`` locks belong to a file handle rather than to a process, and can't be converted
    between shared and exclusive. To behave like ``fcntl`` locks, all backends in a process share
    one handle per file (see ``FILE_TRACKER``) and one OS lock per range, which they upgrade and
    downgrade as needed.

    A zero ``length`` locks everything from ``start`` up to ``GATE_OFFSET``. The file is closed
    whenever the lock isn't held, since Windows can't delete files that are open.
    """

    def __init__(self, path: str, start: int, length: int, debug: bool = False) -> None:
        length = length or GATE_OFFSET - start
        if length <= 0 or start + length > GATE_OFFSET:
            raise ValueError(f"lock range of {path} must be non-empty and end by {GATE_OFFSET}")
        super().__init__(path, start, length, debug=debug)
        #: the lock this backend holds, if any, and whether it holds it for writing
        self._held: Optional[_RangeLock] = None
        self._writer = False

    def __getstate__(self):
        state = super().__getstate__()
        del state["_held"]
        del state["_writer"]
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._held = None
        self._writer = False

    def prepare(self, op: int) -> None:
        try:
            super().prepare(op)
        except BaseException:
            if self._held is None:
                self._close()
            raise

    def poll(self, op: int) -> bool:
        """Try once to acquire the lock in ``op`` mode. Returns whether it was acquired."""
        write = op == LockType.WRITE
        if self._held is not None:
            acquired = self._set_mode(write)
        else:
            if self._file_ref is None:  # closed after a failed attempt
                self.prepare(op)
            acquired = False
            try:
                acquired = self._acquire(write)
            finally:
                if not acquired:
                    self._close()

        if acquired and self.debug:
            self._log_lock_owner(op)
        return acquired

    def release(self) -> None:
        """Release the lock, and unlock the range unless another backend still holds it."""
        held = self._held
        assert held is not None and self._file_ref is not None, "cannot release an unheld lock"
        if held.refs == 1:
            self._unlock_range()
            del _held_locks[(self._file_ref, self._start, self._length)]
        elif self._writer and held.writers == 1:
            self._downgrade()

        held.refs -= 1
        if self._writer:
            held.writers -= 1
        self._held = None
        self._writer = False
        self._close()

    def _acquire(self, write: bool) -> bool:
        """Join the lock this process holds on the range, or take a new one."""
        assert self._file_ref is not None
        key = (self._file_ref, self._start, self._length)
        held = _held_locks.get(key)
        if held is None:
            if not self._lock_new(write):
                return False
            held = _held_locks[key] = _RangeLock()
        elif write and not held.writers and not self._upgrade():
            return False

        held.refs += 1
        if write:
            held.writers += 1
        self._held = held
        self._writer = write
        return True

    def _set_mode(self, write: bool) -> bool:
        """Switch the held lock between reading and writing."""
        held = self._held
        assert held is not None
        if write == self._writer:
            return True

        if write:
            if not held.writers and not self._upgrade():
                return False
            held.writers += 1
        else:
            if held.writers == 1:
                self._downgrade()
            held.writers -= 1
        self._writer = write
        return True

    def _lock_new(self, write: bool) -> bool:
        """Try once to lock the range, which this process doesn't hold yet."""
        if not write:
            return self._lock_range(exclusive=False)

        # Writers take the gate first (see _upgrade)
        if not self._lock_range(exclusive=True, gate=True):
            return False
        try:
            return self._lock_range(exclusive=True)
        finally:
            self._unlock_range(gate=True)

    def _upgrade(self) -> bool:
        """Try once to turn the shared lock this process holds on the range into an exclusive one.

        ``LockFileEx`` can't convert locks, so the shared lock is released before the exclusive
        one is taken. Every writer takes the range's gate first, so while we hold it no writer can
        take the range in between, and if another reader does, our shared lock can be restored.
        """
        if not self._lock_range(exclusive=True, gate=True):
            return False
        try:
            self._unlock_range()
            if self._lock_range(exclusive=True):
                return True
            if not self._lock_range(exclusive=False):
                raise LockError(f"Lost the read lock on {self.path} while upgrading it")
            return False
        finally:
            self._unlock_range(gate=True)

    def _downgrade(self) -> None:
        """Turn the exclusive lock this process holds on the range into a shared one.

        A handle may add a shared lock to a range it holds exclusively, and the first unlock then
        removes the exclusive lock, so the range is never unlocked in between.
        """
        if not self._lock_range(exclusive=False):
            raise LockError(f"Could not downgrade the write lock on {self.path}")
        self._unlock_range()

    def _lock_range(self, exclusive: bool, gate: bool = False) -> bool:
        assert self._file_ref is not None
        offset = self._start + (GATE_OFFSET if gate else 0)
        return _lock_file(self._file_ref.fh.fileno(), exclusive, offset, self._length)

    def _unlock_range(self, gate: bool = False) -> None:
        assert self._file_ref is not None
        offset = self._start + (GATE_OFFSET if gate else 0)
        _unlock_file(self._file_ref.fh.fileno(), offset, self._length)

    def _close(self) -> None:
        if self._file_ref is not None:
            FILE_TRACKER.release(self._file_ref)
            self._file_ref = None
            self._cached_key = None
