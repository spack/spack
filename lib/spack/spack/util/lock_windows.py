# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LockFileEx-based lock backend for Windows, and the ctypes kernel32 bindings it needs."""

import sys

if sys.platform != "win32":
    # Also lets mypy skip this module when run on other platforms.
    raise ImportError("spack.util.lock_windows can only be imported on Windows")

import contextlib
import ctypes
import msvcrt
import os
import signal
import threading
import weakref
from ctypes import wintypes
from typing import Any, Iterator, List, Optional, Tuple

import spack.error
import spack.util.win_acl as win_acl
from spack.util import tty
from spack.util.lock_common import (
    FILE_TRACKER,
    GenericLockBackend,
    LockError,
    LockROFileError,
    OpenFile,
)
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

_kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
]
_kernel32.CreateFileW.restype = wintypes.HANDLE

_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
_kernel32.CloseHandle.restype = wintypes.BOOL

# winerror 32: "The process cannot access the file because it is being used by another
#     process."
# winerror 33: "The process cannot access the file because another process has locked a
#     portion of the file."
_ERROR_SHARING_VIOLATION = 32
_ERROR_LOCK_VIOLATION = 33

# CreateFileW arguments, from the Windows SDK
_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_OPEN_EXISTING = 3
_OPEN_ALWAYS = 4
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


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


def _win_open(path: str, flags: int) -> int:
    """Open a file like ``os.open`` (only ``O_RDONLY``, ``O_RDWR`` and ``O_CREAT`` are supported),
    with the same sharing mode. Unlike ``os.open``, the raised ``OSError`` keeps the Windows error
    code, which is the only way to tell a sharing violation (another program has the file open)
    from a file we may not write to.
    """
    write = bool(flags & os.O_RDWR)
    access = _GENERIC_READ | (_GENERIC_WRITE if write else 0)
    disposition = _OPEN_ALWAYS if flags & os.O_CREAT else _OPEN_EXISTING
    handle = _kernel32.CreateFileW(
        path,
        access,
        _FILE_SHARE_READ | _FILE_SHARE_WRITE,
        None,
        disposition,
        _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        raise OSError(None, ctypes.FormatError(error), path, error)
    try:
        return msvcrt.open_osfhandle(handle, os.O_RDWR if write else os.O_RDONLY)
    except BaseException:
        _kernel32.CloseHandle(handle)
        raise


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


@contextlib.contextmanager
def _deferred_interrupts() -> Iterator[None]:
    """Delay Ctrl-C (``KeyboardInterrupt``) until the end of the block.

    Taking, converting or releasing a lock changes the real OS lock and the bookkeeping that
    records it in several steps. An interrupt between two of them would leave them disagreeing,
    for instance holding an OS lock that nothing will ever release.
    """
    if threading.current_thread() is not threading.main_thread():
        # Python only runs signal handlers in the main thread
        yield
        return

    received: List[Any] = []
    previous = signal.signal(signal.SIGINT, lambda signum, frame: received.append(frame))
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, previous)
        if received:
            if callable(previous):
                previous(signal.SIGINT, received[0])
            elif previous != signal.SIG_IGN:
                raise KeyboardInterrupt


#: Spack lock ranges must lie in ``[0, GATE_OFFSET)``. The upgrade "gate" for the range
#: ``[start, start + length)`` is ``[GATE_OFFSET + start, GATE_OFFSET + start + length)`` of the
#: same file, so the gates of two ranges overlap exactly when the ranges themselves do, and no
#: extra file is needed (Windows allows locking byte ranges beyond the end of a file). Every
#: range Spack locks fits: byte-range locks use offsets of at most 63 bits
#: (``bit_length(sys.maxsize)``), and whole-file locks end at ``GATE_OFFSET``.
#: This is verified on NTFS; filesystems that don't support 64-bit lock offsets (possibly some
#: network shares) may treat gates and the ranges they protect as overlapping.
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
    """Tracks the byte ranges the current process holds real Windows locks on, so that a second
    ``Lock`` in the same process requesting the same range shares the *same* real lock state
    instead of contending with its own process.

    Windows ``LockFileEx`` locks are scoped to the specific *handle* that acquired them, and a
    handle cannot take an exclusive lock on a range that is already locked, even by itself.
    Spack's locking code (e.g. ``FailureTracker``/``SpecLocker`` re-checking a lock it itself
    holds via a second, independent ``Lock`` object, or a plain upgrade/downgrade) would
    otherwise contend with itself.

    Every ``WindowsBackend`` for a given file shares the same open handle (via ``FILE_TRACKER``),
    and this tracker records, per open handle, the one real lock ``mode`` held on each range,
    with reference and writer counts, so the lock state for a range can be updated without
    contention. Locks belong to the handle, so when a handle is closed (and the OS drops its
    locks), its records are dropped as well.

    Only identical ranges are shared: as with ``fcntl`` (see ``Lock``), a process must not hold
    locks on overlapping but different byte ranges of the same file.
    """

    def __init__(self):
        self._groups: "weakref.WeakKeyDictionary[OpenFile, List[WindowsRangeLock]]" = (
            weakref.WeakKeyDictionary()
        )

    def find(self, open_file: OpenFile, start: int, length: int) -> Optional[WindowsRangeLock]:
        """Return the lock held through ``open_file`` on exactly [start, start+length), if any."""
        for group in self._groups.get(open_file, []):
            if group.start == start and group.length == length:
                return group
        return None

    def overlaps(self, open_file: OpenFile, start: int, length: int) -> bool:
        """Whether a lock is held through ``open_file`` on a range that overlaps, but is not
        identical to, [start, start+length)."""
        return any(
            group.start < start + length
            and start < group.start + group.length
            and (group.start, group.length) != (start, length)
            for group in self._groups.get(open_file, [])
        )

    def register(self, open_file: OpenFile, group: WindowsRangeLock) -> None:
        """Record a freshly, really-acquired OS lock as a new group of one."""
        self._groups.setdefault(open_file, []).append(group)

    def forget(self, open_file: OpenFile, group: WindowsRangeLock) -> None:
        """Drop a group that no backend references anymore."""
        groups = self._groups.get(open_file, [])
        if group in groups:
            groups.remove(group)
        if not groups:
            self._groups.pop(open_file, None)


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
    since an open handle prevents other processes from deleting the file (WinError 32). As on
    POSIX, a ``Lock`` that is dropped while holding the lock keeps holding it.
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

    def _open(self, path: str, flags: int) -> int:
        return _win_open(path, flags)

    def _is_transient_open_error(self, error: OSError) -> bool:
        return getattr(error, "winerror", None) == _ERROR_SHARING_VIOLATION

    def prepare(self, op: int) -> None:
        if self._lock_group is not None:
            # While this process holds a lock on the file, the open handle keeps the file from
            # being deleted or replaced, so there's nothing to re-validate, and swapping the
            # handle would drop the lock it holds.
            assert self._file_ref is not None
            if op == LockType.WRITE and self._file_ref.fh.mode == "rb":
                raise LockROFileError(self.path)
            return

        try:
            super().prepare(op)
        except OSError as e:
            self._release_handle()
            if self._is_transient_open_error(e):
                return  # another program has the file open: poll() tries again
            raise
        except BaseException:
            self._release_handle()
            raise

    def poll(self, op: int) -> bool:
        """Attempt to acquire the lock in ``op`` mode in a non-blocking manner. Return whether
        the attempt succeeds.
        """
        with _deferred_interrupts():
            if self._lock_group is not None:
                return self._change_mode(op)

            try:
                if self._file_ref is None:  # not open yet, or released after a failed attempt
                    self.prepare(op)
                    if self._file_ref is None:
                        return False  # another program has the file open
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
        group = WINDOWS_RANGE_LOCK_TRACKER.find(self._file_ref, self._start, self._length)
        if group is None:
            return self._acquire_new(op)

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
        if WINDOWS_RANGE_LOCK_TRACKER.overlaps(self._file_ref, self._start, self._length):
            raise LockError(
                f"Cannot write lock {self.path}[{self._start}:{self._start + self._length}]: "
                "this process holds a lock on an overlapping byte range of the same file"
            )

    def _change_mode(self, op: int) -> bool:
        """Switch the mode this (attached) backend holds its range's lock in."""
        group = self._lock_group
        assert group is not None and self._file_ref is not None
        if group.lost or self._file_ref.fh.closed:
            raise LockError(f"The lock on {self.path} was lost")
        if op == self._mode:
            return True

        if op == LockType.READ:
            if group.writers == 1:
                self._downgrade_to_read(group)
            group.writers -= 1
            self._mode = op
            return True

        if group.mode == LockType.READ and not self._upgrade_to_write(group):
            return False
        group.writers += 1
        self._mode = op
        return True

    def _acquire_new(self, op: int) -> bool:
        """Non-blocking attempt to take a fresh real OS lock on this range: no backend in this
        process currently holds it.
        """
        assert self._file_ref is not None
        if op == LockType.WRITE:
            self._check_no_overlap()
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

        # help for debugging distributed locking
        if self.debug:
            self._log_debug_owner(op)

        self._lock_group = WindowsRangeLock(self._start, self._length, op)
        self._mode = op
        WINDOWS_RANGE_LOCK_TRACKER.register(self._file_ref, self._lock_group)
        return True

    def _log_debug_owner(self, op: int) -> None:
        """Read (and for write locks, record) the PID and host of the lock owner.

        This is best effort: Windows byte-range locks are mandatory, so the owner info at the
        start of the file can't be read or written while another process locks those bytes.
        """
        try:
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
        except OSError as e:
            tty.debug(f"Could not access the lock owner info in {self.path}: {e}", level=2)

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
        self._check_no_overlap()
        if not self._lock_range(LockType.LOCK_EX, gate=True):
            return False

        try:
            # if this fails, the read lock is still held and nothing has changed
            self._unlock_range()

            error: Optional[OSError] = None
            try:
                upgraded = self._lock_range(LockType.LOCK_EX)
            except OSError as e:
                upgraded, error = False, e
            if upgraded:
                group.mode = LockType.WRITE
                return True

            # Another reader holds the range (or locking failed): restore our read lock.
            try:
                restored = self._lock_range(LockType.LOCK_SH)
            except OSError:
                restored = False
            if not restored:
                self._lose(group)
                raise LockError(f"Lost the read lock on {self.path} while upgrading it") from error
            if error is not None:
                raise error
            return False
        finally:
            self._unlock_range(gate=True)

    def _lose(self, group: WindowsRangeLock) -> None:
        """Record that this process no longer holds any OS lock on the group's range."""
        assert self._file_ref is not None
        group.lost = True
        WINDOWS_RANGE_LOCK_TRACKER.forget(self._file_ref, group)

    def _downgrade_to_read(self, group: WindowsRangeLock) -> None:
        """Convert this range's held real exclusive lock to a shared lock without ever releasing
        it.

        A handle may stack a shared lock on a range it holds exclusively, and when the same range
        is locked both ways, the first unlock removes the exclusive lock. So take the shared lock
        (granted immediately, as this handle owns the range) and unlock once. If that unlock
        failed (this handle has just locked the range, so it shouldn't), the range would stay
        exclusively locked, and the extra shared lock would go away when the file is closed.
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
        with _deferred_interrupts():
            group = self._lock_group
            if group is not None:
                assert self._file_ref is not None
                # A lost lock, or one whose file was closed, is no longer held by the OS.
                if not group.lost and not self._file_ref.fh.closed:
                    if group.refs == 1:
                        self._unlock_range()
                        WINDOWS_RANGE_LOCK_TRACKER.forget(self._file_ref, group)
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


#: Groups whose write access to the Spack prefix makes running without locks unsafe, by their
#: SDDL abbreviation and their SID.
_SHARED_GROUPS = {
    "WD": "Everyone",
    "S-1-1-0": "Everyone",
    "AU": "Authenticated Users",
    "S-1-5-11": "Authenticated Users",
    "BU": "Users",
    "S-1-5-32-545": "Users",
}

#: Rights that let a principal create or modify files in a directory: FILE_ADD_FILE,
#: FILE_ADD_SUBDIRECTORY, GENERIC_WRITE and GENERIC_ALL.
_WRITE_RIGHTS = 0x00000002 | 0x00000004 | 0x40000000 | 0x10000000


def check_lock_safety(path: str) -> None:
    """Do some extra checks to ensure disabling locks is safe.

    The Windows counterpart of the POSIX group-/world-writable check: raises an error if the
    current user can write to ``path`` AND its access control list lets one of the groups that
    other users belong to (Everyone, Authenticated Users or Users) create or modify files in it.
    Deny entries are not taken into account, so this errs on the side of refusing.

    This is intended to run on the Spack prefix, but can be run on any path for testing.
    """
    if not os.access(path, os.W_OK):
        return

    groups = sorted(
        {
            _SHARED_GROUPS[ace.sid]
            for ace in win_acl.SecurityDescriptor.from_file(path).dacl
            if ace.ace_type == win_acl.AceType.SDDL_ACCESS_ALLOWED
            and win_acl.AceFlags.SDDL_INHERIT_ONLY not in ace.flags
            and ace.sid in _SHARED_GROUPS
            and (ace.rights or 0) & _WRITE_RIGHTS
        }
    )
    if groups:
        msg = f"Refusing to disable locks: spack is writable by {', '.join(groups)}."
        long_msg = (
            f"Running a shared spack without locks is unsafe. You must "
            f"restrict permissions on {path} or enable locks."
        )
        raise spack.error.SpackError(msg, long_msg)
