# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LockFileEx-based lock backend for Windows, and the ctypes kernel32 bindings it needs.

Split out from ``spack.util.lock`` because mypy (and other tools that type-check on a
non-Windows platform, e.g. Read the Docs) resolve ``ctypes.windll``/``ctypes.wintypes`` against
typeshed's Windows-only stubs, which don't exist for the assumed platform. Type checkers only
skip unreachable code behind a literal ``sys.platform`` comparison, not a derived boolean, so
gating an entire module this way (see ``spack.new_installer_windows`` for the same pattern) is
what actually lets it be skipped.
"""

import sys

if sys.platform != "win32":
    # Also lets mypy skip this module when run on other platforms.
    raise ImportError("spack.util.lock_windows can only be imported on Windows")

import ctypes
import msvcrt
import os
from ctypes import wintypes
from typing import Dict, List, Optional

from spack.util import tty

from .lock import FILE_TRACKER, DevIno, GenericLockBackend, LockType


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


class WindowsRangeLock:
    """The one real ``LockFileEx`` lock for a given byte range in this process, shared by every
    ``WindowsBackend`` that requests an overlapping range while it's held. See
    ``WindowsRangeLockTracker`` for why this is needed.
    """

    __slots__ = ("start", "length", "mode", "refs")

    def __init__(self, start: int, length: int, mode: int):
        self.start = start
        self.length = length
        #: LockType.READ or LockType.WRITE: the real mode currently held, via whichever handle
        #: any attached backend happens to have open
        self.mode = mode
        self.refs = 1


class WindowsRangeLockTracker:
    """Tracks byte ranges the current process holds real Windows locks on, so that a second
    ``Lock`` in the same process requesting an exactly overlapping range shares the *same*
    real lock state instead of contending with its own process.

    Windows ``LockFileEx`` locks are scoped to the specific *handle* that acquired them: two
    different handles regardless of process will compete for lock acquisition.
    Spack's locking code (e.g. ``FailureTracker``/``SpecLocker`` re-checking a lock it
    itself holds via a second, independent ``Lock`` object, or a plain upgrade/downgrade)
    will cause same-process lock contention for the same lock, even with the same handle.

    Every ``WindowsBackend`` for a given range shares the exact same open file handle for the
    underlying file, and this tracker records the one real lock ``mode`` currently held on
    a range in addition to a ref count, so we can accurately track lock usages and update/change
    the lock state for this handle/lock range as needed without contention.
    """

    def __init__(self):
        self._groups: Dict[DevIno, List[WindowsRangeLock]] = {}

    @staticmethod
    def _contains(outer_start: int, outer_length: int, start: int, length: int) -> bool:
        return outer_start <= start and start + length <= outer_start + outer_length

    def find(self, key: DevIno, start: int, length: int) -> Optional[WindowsRangeLock]:
        """Return the group already covering [start, start+length) in this process, if any."""
        for group in self._groups.get(key, []):
            if self._contains(group.start, group.length, start, length):
                return group
        return None

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
#: cross-handle lock requests behave like POSIX fcntl. Unused on POSIX.
WINDOWS_RANGE_LOCK_TRACKER = WindowsRangeLockTracker()


class WindowsBackend(GenericLockBackend):
    """LockFileEx-based lock backend for Windows.

    Like ``PosixBackend``, every ``WindowsBackend`` for a given file shares one open handle via
    the process-wide ``FILE_TRACKER`` (see ``GenericLockBackend._ensure_valid_handle``)
    That alone would be unsafe for Windows locking: unlike ``fcntl``,
    ``LockFileEx``/``UnlockFileEx`` calls apply to whichever handle makes them, so two unrelated
    ``Lock`` objects sharing a handle will compete for the "same" lock, and potentially deadlock.
    ``WINDOWS_RANGE_LOCK_TRACKER`` tracks locks themselves, not FH like FILE_TRACKER, including the
    handle, locking style, and ref counts, so multiple lock attempts from the same process on the
    same range behavemore closely to posix locks.

    There are two other contexts in which Windows diverges from posix

    * *Atomic mode transitions.* ``fcntl`` can convert an already-held lock to a different mode
      (shared <-> exclusive) in place, in a single call. ``LockFileEx`` cannot: there is no
      "convert" operation. ``poll()`` detects a mode transition on an already-held range and
      handles it internally: downgrading a held exclusive lock uses a stack-then-unlock-once
      trick (see ``_downgrade_to_read``); upgrading a held shared lock uses a dedicated per-range
      "gate" lock file to serialize against every other write attempt while the range is briefly,
      fully released and retaken (see ``_upgrade_to_write``).

    * *Per-process (not per-handle) lock scoping.* ``fcntl`` locks are scoped to (process,
      inode): a process can always freely take another lock, in any mode, on a range it already
      holds, via any file descriptor. Because every same-process backend for a range shares the
      same real handle and the same ``WindowsRangeLock``, a mode change made by any one of them
      is immediately visible to all of them -- matching that semantics exactly, with no separate
      "anchor" handle to reason about.

    ``release()`` closes this backend's handle reference (via ``FILE_TRACKER``, closing the
    underlying handle only once every backend sharing it has released) -- needed so a later
    ``cleanup()``/``os.unlink()`` doesn't fail with WinError 32, "used by another process".
    """

    def __init__(self, path: str, start: int, length: int, debug: bool = False) -> None:
        super().__init__(path, start, length, debug=debug)
        #: the WindowsRangeLock this backend belongs to while it holds a lock, None otherwise.
        self._lock_group: Optional[WindowsRangeLock] = None
        #: lazily-created backend for this range's gate file, used only for upgrades.
        self._gate: Optional["WindowsBackend"] = None

    def __getstate__(self):
        state = super().__getstate__()
        del state["_lock_group"]
        del state["_gate"]
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._lock_group = None
        self._gate = None

    def __del__(self) -> None:
        # Guard against a Lock being dropped without an explicit release
        # release properly (respecting shared-group bookkeeping) so a
        # later cleanup()/unlink() doesn't fail with WinError 32, and so we don't leave a
        # same-process WindowsRangeLock group permanently over-referenced.
        if self._file_ref is None:
            return
        try:
            self.release()
        except Exception:
            try:
                FILE_TRACKER.release(self._file_ref)
            except Exception:
                pass
            self._file_ref = None
            self._cached_key = None

    def poll(self, op: int) -> bool:
        """Attempt to acquire the lock in ``op`` mode in a non-blocking manner. Return whether
        the attempt succeeds.
        """
        assert self._file_ref is not None, "cannot poll a lock without the file being set"

        if self._lock_group is not None:
            if op == LockType.READ and self._lock_group.mode == LockType.WRITE:
                self._downgrade_to_read()
                return True
            if op == self._lock_group.mode:
                return True  # already holding at least as much as requested
            return self._upgrade_to_write()  # op == WRITE, mode == READ

        key = self._file_ref.key
        group = WINDOWS_RANGE_LOCK_TRACKER.find(key, self._start, self._length)
        if group is not None:
            self._lock_group = group
            if op == LockType.READ or group.mode == LockType.WRITE:
                group.refs += 1
                return True
            if self._upgrade_to_write():
                group.refs += 1
                return True
            self._lock_group = None
            return False

        return self._acquire_new(key, op)

    def _acquire_new(self, key: DevIno, op: int) -> bool:
        """Non-blocking attempt to take a fresh real OS f-lock on this range: no backend in this
        process currently holds anything overlapping it.
        """
        assert self._file_ref is not None

        handle = _win_handle(self._file_ref.fh.fileno())
        module_op = LockType.to_module(op)
        overlapped = _setup_overlapped(self._start)
        range_low, range_high = _low_high(self._length)

        if not _win_lock_file_ex(
            handle, module_op | LockType.LOCK_NB, range_low, range_high, overlapped
        ):
            return False

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

        self._lock_group = WindowsRangeLock(self._start, self._length, op)
        WINDOWS_RANGE_LOCK_TRACKER.register(key, self._lock_group)
        return True

    def _gate_backend(self) -> "WindowsBackend":
        """The backend for this range's dedicated upgrade "gate" file (see
        ``_upgrade_to_write``), created and opened lazily on first use.
        """
        if self._gate is None:
            self._gate = WindowsBackend(
                self.path + ".gate_lock", self._start, self._length, debug=self.debug
            )
        return self._gate

    def _upgrade_to_write(self) -> bool:
        """Single non-blocking attempt to upgrade this range's currently-held real read lock to
        a write lock.

        ``LockFileEx`` has no atomic convert, and naively dropping the read and retaking
        exclusive would subject spack to races.
        Instead, take a "gate" lock first. Every write acquisition on this
        range takes the same gate first, so while we hold the gate, no other same-process writer
        can be mid-attempt, and only after actually dropping the read do we retake exclusive.
        If that fails, restore the read, which we can guaruntee as we are still behind the gate.

        Note: on Windows the effective timeout for a blocking caller is up to 2x their requested
        timeout, because ``Lock._lock``'s retry loop calls this once per attempt, and each
        attempt both polls the gate and (if granted) polls the primary range.

        Note: the ``.gate_lock`` sidecar file this creates is cleaned up the same way as the
        primary lock file, see ``WindowsBackend.cleanup``.
        """
        assert self._file_ref is not None
        group = self._lock_group
        assert group is not None and group.mode == LockType.READ

        gate = self._gate_backend()
        gate.prepare(LockType.WRITE)
        if not gate.poll(LockType.WRITE):
            return False

        try:
            handle = _win_handle(self._file_ref.fh.fileno())
            range_low, range_high = _low_high(self._length)

            _win_unlock_file_ex(handle, range_low, range_high, _setup_overlapped(self._start))
            if _win_lock_file_ex(
                handle,
                LockType.LOCK_EX | LockType.LOCK_NB,
                range_low,
                range_high,
                _setup_overlapped(self._start),
            ):
                group.mode = LockType.WRITE
                return True

            # A plain reader (no gate needed) raced in during the drop: restore our read.
            _win_lock_file_ex(
                handle,
                LockType.LOCK_SH | LockType.LOCK_NB,
                range_low,
                range_high,
                _setup_overlapped(self._start),
            )
            return False
        finally:
            gate.release()

    def _downgrade_to_read(self) -> None:
        """Convert this range's held real exclusive lock to a shared lock, without ever fully
        releasing it (so no other process can grab exclusive access in the gap caused by a
        lack of atomic lock transitions).

        The win32 locking API has no atomic "convert" operation. But overlapping locks are allowed
        on the same range from the same handle if the exclusive lock is taken first,
        and Windows removes locks in FIFO order. So, stack a shared lock on top of the exclusive
        one already held (this blocking call returns immediately, the handle already owns the
        range, so there's nothing to wait for), then remove one lock, which drops the older
        exclusive lock and leaves the shared one in place. Always succeeds immediately: no gate
        is needed here, unlike upgrading, because the range is never actually unlocked.
        """
        assert self._file_ref is not None
        group = self._lock_group
        assert group is not None and group.mode == LockType.WRITE

        handle = _win_handle(self._file_ref.fh.fileno())
        range_low, range_high = _low_high(self._length)
        _win_lock_file_ex(
            handle, LockType.LOCK_SH, range_low, range_high, _setup_overlapped(self._start)
        )
        _win_unlock_file_ex(handle, range_low, range_high, _setup_overlapped(self._start))
        group.mode = LockType.READ

    def release(self) -> None:
        """Release this backend's interest in the lock, and its ``FILE_TRACKER`` handle
        reference so a later ``cleanup()`` can unlink (closing the underlying handle only once
        every backend sharing it has released it).

        If this was the last backend relying on this range's ``WindowsRangeLock``, performs the
        real OS-level unlock.
        """
        assert self._file_ref is not None, "cannot unlock without the file being set"
        key = self._file_ref.key
        group = self._lock_group
        self._lock_group = None

        if group is not None:
            group.refs -= 1
            if group.refs <= 0:
                WINDOWS_RANGE_LOCK_TRACKER.forget(key, group)
                handle = _win_handle(self._file_ref.fh.fileno())
                range_low, range_high = _low_high(self._length)
                _win_unlock_file_ex(handle, range_low, range_high, _setup_overlapped(self._start))

        FILE_TRACKER.release(self._file_ref)
        self._file_ref = None
        self._cached_key = None

    def cleanup(self, path: str) -> None:
        """Remove the lock file, and its ``.gate_lock`` sidecar (see ``_upgrade_to_write``) if
        one was ever created for it.
        """
        super().cleanup(path)
        try:
            os.unlink(path + ".gate_lock")
        except FileNotFoundError:
            pass
