# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import os
import socket
import stat
import time
from datetime import datetime
from sys import platform as _platform
from types import TracebackType
from typing import IO, Callable, Dict, Generator, List, Optional, Tuple, Type, Union  # novm

import spack.error
from spack.util import lang, tty
from spack.util.string import plural

IS_WINDOWS = _platform == "win32"
if not IS_WINDOWS:
    import fcntl
else:
    import ctypes
    import msvcrt
    from ctypes import wintypes


__all__ = [
    "Lock",
    "LockDowngradeError",
    "LockUpgradeError",
    "LockTransaction",
    "WriteTransaction",
    "ReadTransaction",
    "LockError",
    "LockTimeoutError",
    "LockPermissionError",
    "LockROFileError",
    "CantCreateLockError",
    "PosixBackend",
    "DummyBackend",
]

WHOLE_FILE_RANGE = 0xFFFFFFFF if IS_WINDOWS else 0


ExitFnType = Callable[
    [Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]],
    Optional[bool],
]
ReleaseFnType = Optional[Callable[[], Optional[bool]]]
DevIno = Tuple[int, int]  # (st_dev, st_ino) from os.stat_result


def true_fn() -> bool:
    """A function that always returns True."""
    return True


class OpenFile:
    """Record for keeping track of open lockfiles (with reference counting)."""

    __slots__ = ("fh", "key", "refs")

    def __init__(self, fh: IO[bytes], key: DevIno):
        self.fh = fh
        self.key = key  # (dev, ino)
        self.refs = 0


class OpenFileTracker:
    """Track open lockfiles by inode, to minimize the number of open file descriptors.

    ``fcntl`` locks are associated with an inode. If a process closes *any* file descriptor for an
    inode, all fcntl locks the process holds on that inode are released, even if other descriptors
    for the same inode are still open.

    To avoid accidentally dropping locks we keep at most one open file descriptor per inode and
    reference-count it. The descriptor is only closed when the reference count reaches zero (i.e.
    no ``Lock`` in this process still needs it).

    Descriptors are *not* released on unlock; they are kept alive across lock/unlock cycles so that
    the next lock operation can skip re-opening the file. ``PosixBackend._ensure_valid_handle``
    re-validates the on-disk inode before each lock operation and drops a stale descriptor when
    the file was deleted and replaced.
    """

    def __init__(self):
        self._descriptors: Dict[DevIno, OpenFile] = {}

    def get_ref_for_inode(self, key: DevIno) -> Optional[OpenFile]:
        """Fast lookup: do we already have this inode open?"""
        return self._descriptors.get(key)

    def create_and_track(self, path: str) -> OpenFile:
        """Slow path: Open file, handle directory creation, track it."""
        # Open the file and create it if it doesn't exist (incl. directories).
        try:
            try:
                fd = os.open(path, os.O_RDWR | os.O_CREAT)
                mode = "rb+"
            except PermissionError:
                fd = os.open(path, os.O_RDONLY)
                mode = "rb"
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            # Directory missing, create and retry
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                fd = os.open(path, os.O_RDWR | os.O_CREAT)
            except OSError:
                raise CantCreateLockError(path)
            mode = "rb+"

        # Get file identifier (device, inode) for tracking.
        stat = os.fstat(fd)
        key = (stat.st_dev, stat.st_ino)

        # Did we open a file we already track, e.g. a symlink to existing tracker file.
        if key in self._descriptors:
            os.close(fd)
            existing = self._descriptors[key]
            existing.refs += 1
            return existing

        # Track the new file.
        fh = os.fdopen(fd, mode)
        obj = OpenFile(fh, key)
        obj.refs += 1
        self._descriptors[key] = obj
        return obj

    def release(self, open_file: OpenFile):
        """Decrement the reference count and close the file handle when it reaches zero."""
        open_file.refs -= 1
        if open_file.refs <= 0:
            if self._descriptors.get(open_file.key) is open_file:
                del self._descriptors[open_file.key]
            open_file.fh.close()

    def purge(self):
        """Close all tracked file descriptors and clear the cache."""
        for open_file in self._descriptors.values():
            open_file.fh.close()
        self._descriptors.clear()


#: Open file descriptors for locks in this process. Used to prevent one process
#: from opening the sam file many times for different byte range locks
FILE_TRACKER = OpenFileTracker()


class WindowsRangeLock:
    """One real ``LockFileEx`` lock, (virtually) shared by every ``WindowsBackend`` in this
    process that requests a range contained in it while it's held. See
    ``WindowsRangeLockTracker`` for why this is needed.
    """

    __slots__ = ("start", "length", "anchor", "refs")

    def __init__(self, start: int, length: int, anchor: "WindowsBackend"):
        self.start = start
        self.length = length
        #: the WindowsBackend whose handle actually holds the OS-level lock
        self.anchor = anchor
        self.refs = 1


class WindowsRangeLockTracker:
    """Tracks byte ranges the current process holds real Windows locks on, so a second
    ``Lock``/handle in the same process requesting an overlapping range doesn't contend with its
    own process.

    POSIX ``fcntl`` locks are scoped to (process, inode): a process can always freely take
    another lock -- in any mode -- on a range it already holds, via any file descriptor, because
    the OS only ever tracks one lock per (process, inode, range). Windows ``LockFileEx`` locks
    are scoped to the specific *handle* that acquired them: two different handles in the same
    process genuinely contend, even though they're logically "the same owner". Spack's locking
    code (e.g. ``FailureTracker``/``SpecLocker`` re-checking a lock it itself holds via a second,
    independent ``Lock`` object) is written against POSIX's semantics, so without this, those
    same-process checks deadlock on Windows instead of trivially succeeding.

    When a request is contained in a range already held (for real) by this process, it is
    granted immediately without ever calling ``LockFileEx`` ("shadow" grant, tracked here by
    incrementing the group's refcount) -- the pre-existing real lock already excludes other
    processes, which is all a second in-process handle needs. Only the first request for a range
    takes the real OS lock; only the last release (real or shadow, across the whole group) drops
    it, using whichever handle (the "anchor") actually holds it -- which may not be the handle
    that happens to trigger that last release, if the anchor itself released earlier while
    shadow holders were still active. See ``WindowsBackend.release``.
    """

    def __init__(self):
        self._groups: Dict[DevIno, List[WindowsRangeLock]] = {}

    @staticmethod
    def _contains(outer_start: int, outer_length: int, start: int, length: int) -> bool:
        return outer_start <= start and start + length <= outer_start + outer_length

    def try_join(self, key: DevIno, start: int, length: int) -> Optional[WindowsRangeLock]:
        """If this process already holds a real lock covering [start, start+length), join that
        group (bumping its refcount) and return it. Otherwise return None: the caller must take
        a real OS lock itself and register it with ``register``.
        """
        for group in self._groups.get(key, []):
            if self._contains(group.start, group.length, start, length):
                group.refs += 1
                return group
        return None

    def register(self, key: DevIno, start: int, length: int, anchor: "WindowsBackend"):
        """Record a freshly, really-acquired OS lock as a new group of one."""
        group = WindowsRangeLock(start, length, anchor)
        self._groups.setdefault(key, []).append(group)
        return group

    def release(self, key: DevIno, group: WindowsRangeLock) -> bool:
        """Drop one reference to ``group``. Returns True if this was the last one, meaning the
        caller must now perform the real OS-level unlock (via ``group.anchor``).
        """
        group.refs -= 1
        if group.refs <= 0:
            groups = self._groups.get(key, [])
            if group in groups:
                groups.remove(group)
            if not groups:
                self._groups.pop(key, None)
            return True
        return False


#: Tracks real Windows byte-range locks held by this process, to make same-process,
#: cross-handle lock requests behave like POSIX fcntl. Unused on POSIX.
WINDOWS_RANGE_LOCK_TRACKER = WindowsRangeLockTracker()


def _attempts_str(wait_time, nattempts):
    # Don't print anything if we succeeded on the first try
    if nattempts <= 1:
        return ""

    attempts = plural(nattempts, "attempt")
    return " after {} and {}".format(lang.pretty_seconds(wait_time), attempts)


class LockType:
    READ = 0
    WRITE = 1

    # Platform-native flag constants, merged directly onto LockType so backends and callers
    # share one vocabulary regardless of platform.
    LOCK_CATCH: Type[Exception]
    if IS_WINDOWS:
        # From the Windows SDK (winbase.h): not exposed by ctypes, so hardcoded here.
        LOCK_SH = 0  # shared lock is the default (absence of the exclusive flag)
        LOCK_EX = 0x00000002  # LOCKFILE_EXCLUSIVE_LOCK
        LOCK_NB = 0x00000001  # LOCKFILE_FAIL_IMMEDIATELY
        # No LOCK_CATCH: WindowsBackend checks LockFileEx's return value directly (see
        # _win_lock_file_ex) instead of catching an exception for the "already locked" case.
    else:
        LOCK_SH = fcntl.LOCK_SH
        LOCK_EX = fcntl.LOCK_EX
        LOCK_NB = fcntl.LOCK_NB
        LOCK_UN = fcntl.LOCK_UN
        LOCK_CATCH = OSError

    @staticmethod
    def to_str(tid):
        ret = "READ"
        if tid == LockType.WRITE:
            ret = "WRITE"
        return ret

    @staticmethod
    def to_module(tid):
        lock = LockType.LOCK_SH
        if tid == LockType.WRITE:
            lock = LockType.LOCK_EX
        return lock

    @staticmethod
    def is_valid(op: int) -> bool:
        return op == LockType.READ or op == LockType.WRITE


class GenericLockBackend:
    """Base class for platform lock backends.

    Handles bookkeeping shared by all backends: tracking the open file handle through
    ``FILE_TRACKER`` and reading/writing the debug PID/host header. Subclasses implement the
    actual OS-level locking primitives (``poll()`` and ``release()``).
    """

    def __init__(self, path: str, start: int, length: int, debug: bool = False) -> None:
        self.path = path
        self._start = start
        self._length = length
        self.debug = debug
        self._file_ref: Optional[OpenFile] = None
        self._cached_key: Optional[DevIno] = None
        # PID and host of the lock holder (only used in debug mode)
        self.pid: Optional[int] = None
        self.old_pid: Optional[int] = None
        self.host: Optional[str] = None
        self.old_host: Optional[str] = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_file_ref"]
        del state["_cached_key"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._file_ref = None
        self._cached_key = None

    def _ensure_valid_handle(self) -> IO[bytes]:
        """Return a valid file handle for the lock file, opening or re-opening as needed.

        On the happy path this costs a single ``os.stat`` syscall: if the inode on disk matches
        ``_cached_key``, the already-open file handle is returned immediately.

        If the inode changed (the lock file was deleted and replaced by another process), the stale
        reference is released and a fresh one is obtained.  If the file does not exist yet it is
        created (along with any missing parent directories).
        """
        try:
            # Check what is currently on disk. This is the only syscall in the happy path.
            stat_res = os.stat(self.path)
            current_key = (stat_res.st_dev, stat_res.st_ino)

            # Double-check that our cache corresponds the file on disk.
            if self._file_ref and not self._file_ref.fh.closed:
                if self._cached_key == current_key:
                    return self._file_ref.fh

                # Stale path: file was deleted and replaced on disk.
                FILE_TRACKER.release(self._file_ref)
                self._file_ref = None

            # Get reference to the verified inode from the tracker if it exist, or a new one.
            existing_ref = FILE_TRACKER.get_ref_for_inode(current_key)
            if existing_ref:
                self._file_ref = existing_ref
                self._file_ref.refs += 1
            else:
                # We don't have it tracked, so we need to open and track it ourselves.
                self._file_ref = FILE_TRACKER.create_and_track(self.path)
        except OSError as e:
            # Re-raise all errors except for "file not found".
            if e.errno != errno.ENOENT:
                raise

            # File was not found, so remove it from our cache.
            if self._file_ref:
                FILE_TRACKER.release(self._file_ref)
                self._file_ref = None

            self._file_ref = FILE_TRACKER.create_and_track(self.path)

        # Update our local cache of what we hold
        self._cached_key = self._file_ref.key

        return self._file_ref.fh

    def prepare(self, op: int) -> None:
        """Ensure the lock file is open; raise if a write lock is requested on a read-only file."""
        fh = self._ensure_valid_handle()

        if LockType.to_module(op) == LockType.LOCK_EX and fh.mode == "rb":
            # Attempt to upgrade to write lock w/a read-only file.
            # If the file were writable, we'd have opened it rb+
            raise LockROFileError(self.path)

    def cleanup(self, path: str) -> None:
        """Remove the lock file."""
        os.unlink(path)

    def _read_log_debug_data(self) -> None:
        """Read PID and host data out of the file if it is there."""
        assert self._file_ref is not None, "cannot read debug log without the file being set"

        self.old_pid = self.pid
        self.old_host = self.host

        self._file_ref.fh.seek(0)
        line = self._file_ref.fh.read()
        if line:
            pid, host = line.decode("utf-8").strip().split(",")
            _, _, pid = pid.rpartition("=")
            _, _, self.host = host.rpartition("=")
            self.pid = int(pid)

    def _write_log_debug_data(self) -> None:
        """Write PID and host data to the file, recording old values."""
        assert self._file_ref is not None, "cannot write debug log without the file being set"

        self.old_pid = self.pid
        self.old_host = self.host

        self.pid = os.getpid()
        self.host = socket.gethostname()
        # write pid, host to disk to sync over FS
        self._file_ref.fh.seek(0)
        self._file_ref.fh.write(f"pid={self.pid},host={self.host}".encode("utf-8"))
        self._file_ref.fh.truncate()
        self._file_ref.fh.flush()
        os.fsync(self._file_ref.fh.fileno())

    def poll(self, op: int) -> bool:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError


class PosixBackend(GenericLockBackend):
    """fcntl-based lock backend for POSIX systems."""

    def poll(self, op: int) -> bool:
        """Attempt to acquire the lock in a non-blocking manner. Return whether
        the locking attempt succeeds
        """
        assert self._file_ref is not None, "cannot poll a lock without the file being set"
        fh = self._file_ref.fh.fileno()
        module_op = LockType.to_module(op)

        try:
            # Try to get the lock (will raise if not available.)
            fcntl.lockf(fh, module_op | LockType.LOCK_NB, self._length, self._start, os.SEEK_SET)

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

            return True

        except LockType.LOCK_CATCH as e:
            # EAGAIN and EACCES == locked by another process (so try again)
            if self._lock_fail_condition(e):
                raise

        return False

    def _lock_fail_condition(self, e) -> bool:
        return e.errno not in (errno.EAGAIN, errno.EACCES)

    def release(self) -> None:
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may be masquerading as write
        locks, but this removes either.

        Unlike ``WindowsBackend.release``, this does not close the tracked file handle: fcntl
        locks are released independently of the descriptor, and keeping the handle open lets the
        next lock/unlock cycle skip re-opening the file (see ``OpenFileTracker``).
        """
        assert self._file_ref is not None, "cannot unlock without the file being set"
        fcntl.lockf(
            self._file_ref.fh.fileno(), LockType.LOCK_UN, self._length, self._start, os.SEEK_SET
        )


def _low_high(value):
    low = value & 0xFFFFFFFF
    high = (value >> 32) & 0xFFFFFFFF
    return low, high


if IS_WINDOWS:
    # Minimal ctypes bindings for the pieces of the Win32 file-locking API this module needs
    # (LockFileEx/UnlockFileEx), so Windows support has no third-party dependency (e.g. pywin32).

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


class WindowsBackend(GenericLockBackend):
    """LockFileEx-based lock backend for Windows.

    This backend alone is responsible for making Windows locking behave like the POSIX ``fcntl``
    locking the rest of ``lock.py`` (and the callers of ``Lock``) is written against. The shared
    ``Lock`` frontend and ``PosixBackend`` never need to know any of this: they only ever call
    the generic ``prepare``/``poll``/``release`` interface. Two POSIX properties don't hold on
    Windows, and are restored here rather than exposed upward:

    * *Atomic mode transitions.* ``fcntl`` can convert an already-held lock to a different mode
      (shared <-> exclusive) in place, in a single call. ``LockFileEx`` cannot: there is no
      "convert" operation. ``poll()`` detects a mode transition on an already-held handle
      (tracked via ``_held_op``) and handles it internally: downgrading a held exclusive lock
      uses a stack-then-unlock-once trick (see ``_downgrade_to_read``); upgrading a held shared
      lock uses a dedicated per-range "gate" lock file to serialize against every other write
      attempt while the range is briefly, fully released and retaken (see ``_upgrade_to_write``).

    * *Per-process (not per-handle) lock scoping.* ``fcntl`` locks are scoped to (process,
      inode): a process can always freely take another lock, in any mode, on a range it already
      holds, via any file descriptor. ``LockFileEx`` locks are scoped to the specific handle that
      acquired them: two different handles in the same process genuinely contend, even though
      they're logically "the same owner". ``poll()`` consults ``WINDOWS_RANGE_LOCK_TRACKER`` to
      grant such same-process requests immediately instead of contending with itself.

    Relatedly, unlike ``PosixBackend`` (where sharing a handle across ``Lock`` objects via the
    process-wide ``FILE_TRACKER`` is safe and desirable, since ``fcntl`` locks are scoped to the
    process/inode), this backend never shares its handle with another backend instance: doing so
    would make two unrelated ``Lock`` objects on the same path silently share one another's
    locks. Each ``WindowsBackend`` opens and owns its own private handle, and ``release()``
    usually closes it (also needed so a later ``cleanup()``/``os.unlink()`` doesn't fail with
    WinError 32, "used by another process") -- except when other same-process handles still
    depend on it being open, per ``WINDOWS_RANGE_LOCK_TRACKER``.
    """

    def __init__(self, path: str, start: int, length: int, debug: bool = False) -> None:
        super().__init__(path, start, length, debug=debug)
        #: the WindowsRangeLock group this backend belongs to while it holds a lock (real or
        #: shadow -- see WindowsRangeLockTracker), None otherwise.
        self._lock_group: Optional[WindowsRangeLock] = None
        #: LockType.READ or LockType.WRITE if this handle currently holds a lock, else None.
        self._held_op: Optional[int] = None
        #: lazily-created backend for this range's gate file, used only for upgrades.
        self._gate: Optional["WindowsBackend"] = None

    def __getstate__(self):
        # _lock_group/_held_op/_gate are process-local bookkeeping (like _file_ref/_cached_key,
        # which the base class already strips): meaningless -- and actively dangerous, see
        # __setstate__ -- in a different process, e.g. when a Lock crosses a
        # multiprocessing.Process boundary.
        state = super().__getstate__()
        del state["_lock_group"]
        del state["_held_op"]
        del state["_gate"]
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        # A stale _held_op surviving unpickling would make poll() think this fresh handle (in
        # the new process) already holds a lock in some mode, misrouting it into the upgrade/
        # downgrade paths instead of a normal fresh acquire.
        self._lock_group = None
        self._held_op = None
        self._gate = None

    def _ensure_valid_handle(self) -> IO[bytes]:
        """Return this backend's own file handle, opening it if necessary."""
        if self._file_ref is not None and not self._file_ref.fh.closed:
            return self._file_ref.fh

        try:
            try:
                fd = os.open(self.path, os.O_RDWR | os.O_CREAT)
                mode = "rb+"
            except PermissionError:
                fd = os.open(self.path, os.O_RDONLY)
                mode = "rb"
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            try:
                fd = os.open(self.path, os.O_RDWR | os.O_CREAT)
                mode = "rb+"
            except OSError:
                raise CantCreateLockError(self.path)

        fh = os.fdopen(fd, mode)
        stat_res = os.fstat(fd)
        self._file_ref = OpenFile(fh, (stat_res.st_dev, stat_res.st_ino))
        self._cached_key = self._file_ref.key
        return fh

    def __del__(self) -> None:
        # Guard against a Lock being dropped without an explicit release (e.g. a test that
        # raises before cleanup): release properly (respecting shared-group bookkeeping) so a
        # later cleanup()/unlink() doesn't fail with WinError 32, and so we don't leave a
        # same-process WindowsRangeLock group permanently over-referenced.
        if self._file_ref is None:
            return
        try:
            self.release()
        except Exception:
            try:
                self._file_ref.fh.close()
            except Exception:
                pass
        self._file_ref = None
        self._cached_key = None

    def poll(self, op: int) -> bool:
        """Attempt to acquire the lock in ``op`` mode in a non-blocking manner. Return whether
        the attempt succeeds.

        This is the single entry point ``Lock`` calls for every acquire, upgrade, and downgrade
        (each is just a possibly-repeated non-blocking ``poll()``, per the generic backoff loop
        in ``Lock._lock``): it dispatches on what this handle currently holds, if anything.
        """
        assert self._file_ref is not None, "cannot poll a lock without the file being set"

        if self._held_op == op:
            return True  # already holding this exact mode via this handle
        if self._held_op == LockType.READ and op == LockType.WRITE:
            return self._upgrade_to_write()
        if self._held_op == LockType.WRITE and op == LockType.READ:
            self._downgrade_to_read()
            return True

        return self._poll_acquire(op)

    def _poll_acquire(self, op: int) -> bool:
        """Non-blocking attempt to acquire ``op``.

        If this handle has never held a lock (``_lock_group is None``), and this process already
        holds a real lock covering this range via some *other* handle, join it instead of asking
        Windows to grant a second, conflicting lock to a different handle in the same process.
        See ``WindowsRangeLockTracker``. If this handle already has a group (a real or shadow
        hold from an earlier call), that check is skipped: this handle already has its own
        standing with the OS (or is riding on another handle's), so it talks to the OS directly.
        """
        assert self._file_ref is not None

        if self._lock_group is None:
            joined = WINDOWS_RANGE_LOCK_TRACKER.try_join(
                self._file_ref.key, self._start, self._length
            )
            if joined is not None:
                self._lock_group = joined
                self._held_op = op
                return True

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

        if self._lock_group is None:
            self._lock_group = WINDOWS_RANGE_LOCK_TRACKER.register(
                self._file_ref.key, self._start, self._length, self
            )
        self._held_op = op
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
        """Single non-blocking attempt to upgrade this handle's currently-held read to a write.

        ``LockFileEx`` has no atomic convert, and naively dropping the read and retaking
        exclusive would open a window where another process could grab the range in between. To
        close that window: take a dedicated "gate" lock first. Every write acquisition on this
        range -- fresh, nested, or an upgrade -- takes the same gate first (see ``_poll_acquire``
        joining an in-process real hold), so while we hold the gate, no other same-process writer
        can be mid-attempt, and only after actually dropping our read do we retake exclusive. If
        that fails, restore the read (can only happen if a plain, non-upgrading reader raced in
        during the drop; readers don't need the gate).

        Note: on Windows the effective timeout for a blocking caller is up to 2x their requested
        timeout, because ``Lock._lock``'s retry loop calls this once per attempt, and each
        attempt both polls the gate and (if granted) polls the primary range.

        Note: the ``.gate_lock`` sidecar file this creates is cleaned up the same way as the
        primary lock file -- see ``WindowsBackend.cleanup``.

        Declines (returns False) if this handle's read is currently shared with other
        same-process holders (``WindowsRangeLock`` group refcount > 1): relinquishing it would
        invalidate their lock out from under them. The caller (``Lock._lock``'s retry loop) will
        simply try again later, once that sharing clears.
        """
        if self._lock_group is not None and self._lock_group.refs > 1:
            return False

        gate = self._gate_backend()
        gate.prepare(LockType.WRITE)
        if not gate.poll(LockType.WRITE):
            return False

        try:
            self.release()
            self.prepare(LockType.WRITE)
            if self._poll_acquire(LockType.WRITE):
                return True
            self.prepare(LockType.READ)
            self._poll_acquire(LockType.READ)
            return False
        finally:
            gate.release()

    def _downgrade_to_read(self) -> None:
        """Convert a held exclusive lock to a shared lock on this handle, without ever fully
        releasing it (so no other process can grab exclusive access in the gap).

        ``LockFileEx`` has no atomic "convert" operation. But overlapping locks are allowed on
        the same range from the same handle, and Windows removes locks in FIFO
        (first-acquired-first-removed) order. So: stack a shared lock on top of the exclusive
        one already held (this blocking call returns immediately -- the same handle already
        owns the range, so there's nothing to wait for), then remove one lock, which drops the
        older exclusive lock and leaves the shared one in place. Always succeeds immediately: no
        gate is needed here, unlike upgrading, because the range is never actually unlocked.

        No-op (beyond updating our own bookkeeping) if this handle is a "shadow" holder (see
        ``WindowsRangeLockTracker``): it never took a real exclusive lock itself, so there's
        nothing to convert.
        """
        assert self._file_ref is not None
        if self._lock_group is None or self._lock_group.anchor is self:
            handle = _win_handle(self._file_ref.fh.fileno())
            range_low, range_high = _low_high(self._length)
            _win_lock_file_ex(
                handle, LockType.LOCK_SH, range_low, range_high, _setup_overlapped(self._start)
            )
            _win_unlock_file_ex(handle, range_low, range_high, _setup_overlapped(self._start))
        self._held_op = LockType.READ

    def _real_unlock(self) -> None:
        """Perform the actual OS-level unlock on this handle. Only ever called on the group's
        anchor -- the one handle that actually holds the real ``LockFileEx`` lock.
        """
        assert self._file_ref is not None
        handle = _win_handle(self._file_ref.fh.fileno())
        overlapped = _setup_overlapped(self._start)
        range_low, range_high = _low_high(self._length)
        _win_unlock_file_ex(handle, range_low, range_high, overlapped)

    def release(self) -> None:
        """Release the lock and (usually) close the tracked handle so a later ``cleanup()`` can
        unlink.

        Most releases are simple: this handle is the sole (real) holder, so it does the real
        unlock and closes its handle. But when several ``WindowsBackend``\\ s in this process
        share a ``WindowsRangeLock`` group (see ``WindowsRangeLockTracker``), only the *last*
        one to release may perform the real unlock -- and only the group's *anchor* handle
        actually holds that real lock. If the anchor itself releases first, its handle is kept
        open (deferred) so the lock stays valid for the remaining same-process holders, until
        whichever of them releases last triggers the real unlock via the anchor.
        """
        assert self._file_ref is not None, "cannot unlock without the file being set"
        key = self._file_ref.key
        group = self._lock_group
        self._lock_group = None
        self._held_op = None

        if group is None:
            # No self-lock bookkeeping (shouldn't happen via the normal Lock/poll path): this
            # handle must hold the real lock itself.
            self._real_unlock()
            self._file_ref.fh.close()
            self._file_ref = None
            return

        is_last = WINDOWS_RANGE_LOCK_TRACKER.release(key, group)
        is_anchor = group.anchor is self

        if is_last:
            # The anchor holds the one real lock for the whole group, regardless of which
            # backend triggered this final release.
            group.anchor._real_unlock()
            if group.anchor._file_ref is not None:
                group.anchor._file_ref.fh.close()
                group.anchor._file_ref = None

        if (not is_anchor or is_last) and self._file_ref is not None:
            # Close our own handle -- unless we're the anchor and other same-process holders
            # remain, in which case our handle *is* the real lock and must stay open for them.
            self._file_ref.fh.close()
            self._file_ref = None

    def cleanup(self, path: str) -> None:
        """Remove the lock file, and its ``.gate_lock`` sidecar (see ``_upgrade_to_write``) if
        one was ever created for it.
        """
        super().cleanup(path)
        try:
            os.unlink(path + ".gate_lock")
        except FileNotFoundError:
            pass


class DummyBackend(GenericLockBackend):
    """No-op lock backend: all operations succeed without acquiring any real locks."""

    def __init__(self) -> None:  # doesn't need path/start/length: nothing is ever tracked
        pass

    def prepare(self, op: int) -> None:
        pass

    def poll(self, op: int) -> bool:
        return True

    def release(self) -> None:
        pass

    def cleanup(self, path: str) -> None:
        pass


BackendType = Union[PosixBackend, WindowsBackend, DummyBackend]


def platform_lock_backend(path, start, length, debug) -> BackendType:
    """Per platform dispatch for lock backend implementation"""
    if IS_WINDOWS:
        return WindowsBackend(path, start, length, debug=debug)
    else:
        return PosixBackend(path, start, length, debug=debug)


class Lock:
    """This is an implementation of a filesystem lock using Python's lockf.

    In Python, ``lockf`` actually calls ``fcntl``, so this should work with any filesystem
    implementation that supports locking through the fcntl calls. This includes distributed
    filesystems like Lustre (when flock is enabled) and recent NFS versions.

    Note that this is for managing contention over resources *between* processes and not for
    managing contention between threads in a process: the functions of this object are not
    thread-safe. A process also must not maintain multiple locks on the same file (or, more
    specifically, on overlapping byte ranges in the same file).
    """

    def __init__(
        self,
        path: str,
        *,
        start: int = 0,
        length: int = 0,
        default_timeout: Optional[float] = None,
        debug: bool = False,
        desc: str = "",
        enable: bool = True,
    ) -> None:
        """Construct a new lock on the file at ``path``.

        By default, the lock applies to the whole file.  Optionally, caller can specify a byte
        range beginning ``start`` bytes from the start of the file and extending ``length`` bytes
        from there.

        This exposes a subset of fcntl locking functionality.  It does not currently expose the
        ``whence`` parameter -- ``whence`` is always ``os.SEEK_SET`` and ``start`` is always
        evaluated from the beginning of the file.

        Args:
            path: path to the lock
            start: optional byte offset at which the lock starts
            length: optional number of bytes to lock
            default_timeout: seconds to wait for lock attempts, where None means to wait
                indefinitely
            debug: debug mode specific to locking
            desc: optional debug message lock description, which is helpful for distinguishing
                between different Spack locks.
            enable: when False, swap in a no-op backend so all lock operations succeed
                without acquiring a real filesystem lock.
        """
        self.path = path
        self._reads = 0
        self._writes = 0

        # byte range parameters. A zero length means "lock to the end of the file" on POSIX,
        # but Windows has no such convention -- LockFileEx always needs an explicit range -- so
        # a length of 0 is normalized to WHOLE_FILE_RANGE there.
        self._start = start
        self._length = length or WHOLE_FILE_RANGE

        # enable debug mode
        self.debug = debug

        # optional debug description
        self.desc = f" ({desc})" if desc else ""

        # If the user doesn't set a default timeout, or if they choose
        # None, 0, etc. then lock attempts will not time out (unless the
        # user sets a timeout for each attempt)
        self.default_timeout = default_timeout or None

        if enable:
            self.backend: BackendType = platform_lock_backend(
                path, start, self._length, debug=debug
            )
        else:
            self.backend = DummyBackend()

    @staticmethod
    def _poll_interval_generator(
        _wait_times: Optional[Tuple[float, float, float]] = None,
    ) -> Generator[float, None, None]:
        """This implements a backoff scheme for polling a contended resource by suggesting a
        succession of wait times between polls.

        It suggests a poll interval of .1s until 2 seconds have passed, then a poll interval of
        .2s until 10 seconds have passed, and finally (for all requests after 10s) suggests a poll
        interval of .5s.

        This doesn't actually track elapsed time, it estimates the waiting time as though the
        caller always waits for the full length of time suggested by this function.
        """
        num_requests = 0
        stage1, stage2, stage3 = _wait_times or (1e-1, 2e-1, 5e-1)
        wait_time = stage1
        while True:
            if num_requests >= 60:  # 40 * .2 = 8
                wait_time = stage3
            elif num_requests >= 20:  # 20 * .1 = 2
                wait_time = stage2
            num_requests += 1
            yield wait_time

    def __repr__(self) -> str:
        """Formal representation of the lock."""
        rep = f"{self.__class__.__name__}("
        for attr, value in self.__dict__.items():
            rep += f"{attr}={value.__repr__()}, "
        return f"{rep.strip(', ')})"

    def __str__(self) -> str:
        """Readable string (with key fields) of the lock."""
        location = f"{self.path}[{self._start}:{self._length}]"
        timeout = f"timeout={self.default_timeout}"
        activity = f"#reads={self._reads}, #writes={self._writes}"
        return f"({location}, {timeout}, {activity})"

    def __getstate__(self):
        """Don't include counts in pickled state (backend handles its own file handles)."""
        state = self.__dict__.copy()
        del state["_reads"]
        del state["_writes"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._reads = 0
        self._writes = 0

    def _poll_lock(self, op: int) -> bool:
        """Direct pass-through to the backend's single non-blocking lock attempt."""
        return self.backend.poll(op)

    def _lock(self, op: int, timeout: Optional[float] = None) -> Tuple[float, int]:
        """This takes a lock using POSIX locks (``fcntl.lockf``).

        The lock is implemented as a spin lock using a nonblocking call to ``lockf()``.

        If the lock times out, it raises a ``LockError``. If the lock is successfully acquired, the
        total wait time and the number of attempts is returned.
        """
        assert LockType.is_valid(op)
        op_str = LockType.to_str(op)

        self._log_acquiring("{0} LOCK".format(op_str))
        timeout = timeout or self.default_timeout

        self.backend.prepare(op)

        self._log_debug(
            "{} locking [{}:{}]: timeout {}".format(
                op_str.lower(), self._start, self._length, lang.pretty_seconds(timeout or 0)
            )
        )

        start_time = time.monotonic()
        end_time = float("inf") if not timeout else start_time + timeout
        num_attempts = 1
        poll_intervals = Lock._poll_interval_generator()

        while True:
            if self.backend.poll(op):
                return time.monotonic() - start_time, num_attempts
            if time.monotonic() >= end_time:
                break
            time.sleep(next(poll_intervals))
            num_attempts += 1

        raise LockTimeoutError(op, self.path, time.monotonic() - start_time, num_attempts)

    def acquire_read(self, timeout: Optional[float] = None) -> bool:
        """Acquires a recursive, shared lock for reading.

        Read and write locks can be acquired and released in arbitrary order, but the POSIX lock is
        held until all local read and write locks are released.

        Returns True if it is the first acquire and actually acquires the POSIX lock, False if it
        is a nested transaction.
        """
        timeout = timeout or self.default_timeout

        if self._reads == 0 and self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.READ, timeout=timeout)
            self._reads += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired("READ LOCK", wait_time, nattempts)
            return True
        else:
            # Increment the read count for nested lock tracking
            self._reaffirm_lock()
            self._reads += 1
            return False

    def acquire_write(self, timeout: Optional[float] = None) -> bool:
        """Acquires a recursive, exclusive lock for writing.

        Read and write locks can be acquired and released in arbitrary order, but the POSIX lock
        is held until all local read and write locks are released.

        Returns True if it is the first acquire and actually acquires the POSIX lock, False if it
        is a nested transaction.
        """
        timeout = timeout or self.default_timeout

        if self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.WRITE, timeout=timeout)
            self._writes += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired("WRITE LOCK", wait_time, nattempts)

            # return True only if we weren't nested in a read lock.
            # TODO: we may need to return two values: whether we got
            # the write lock, and whether this is acquiring a read OR
            # write lock for the first time. Now it returns the latter.
            return self._reads == 0
        else:
            # Increment the write count for nested lock tracking
            self._reaffirm_lock()
            self._writes += 1
            return False

    def _reaffirm_lock(self) -> None:
        """Fork-safety: always re-affirm the lock with one non-blocking attempt. In the same
        process, re-locking an already-held byte range succeeds instantly (POSIX). In a forked
        child that doesn't own the POSIX lock, the call fails immediately and we raise. Use WRITE
        if we hold an exclusive lock so we don't accidentally downgrade it.

        No-op on Windows (Spawn only)
        """
        if IS_WINDOWS:
            return
        if self._writes > 0:
            op = LockType.WRITE
        elif self._reads > 0:
            op = LockType.READ
        else:
            return
        self.backend.prepare(op)
        if not self.backend.poll(op):
            raise LockTimeoutError(op, self.path, time=0, attempts=1)

    def try_acquire_read(self) -> bool:
        """Non-blocking attempt to acquire a shared read lock.

        Returns True if the lock was acquired, False if it would block.
        """
        if self._reads == 0 and self._writes == 0:
            self.backend.prepare(LockType.READ)
            if not self.backend.poll(LockType.READ):
                return False
            self._reads += 1
            self._log_acquired("READ LOCK", 0, 1)
            return True
        else:
            self._reaffirm_lock()
            self._reads += 1
            return True

    def try_acquire_write(self) -> bool:
        """Non-blocking attempt to acquire an exclusive write lock.

        Returns True if the lock was acquired, False if it would block.
        Handles three cases: no lock held (fresh acquire), read held (upgrade -- fully replaces
        the read with a write, unlike the nested behavior of ``acquire_write``), or write already
        held (nested).
        """
        if self._writes == 0:
            self.backend.prepare(LockType.WRITE)
            if not self.backend.poll(LockType.WRITE):
                return False
            self._reads = 0
            self._writes = 1
            self._log_acquired("WRITE LOCK", 0, 1)
            return True
        else:
            self._reaffirm_lock()
            self._writes += 1
            return True

    def is_write_locked(self) -> bool:
        """Returns ``True`` if the path is write locked, otherwise, ``False``"""
        try:
            self.acquire_read()

            # If we have a read lock then no other process has a write lock.
            self.release_read()
        except LockTimeoutError:
            # Another process is holding a write lock on the file
            return True

        return False

    def downgrade_write_to_read(self, timeout: Optional[float] = None) -> None:
        """Downgrade from an exclusive write lock to a shared read.

        Raises:
            LockDowngradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._writes == 1 and self._reads == 0:
            self._log_downgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.READ, timeout=timeout)
            self._reads = 1
            self._writes = 0
            self._log_downgraded(wait_time, nattempts)
        else:
            raise LockDowngradeError(self.path)

    def upgrade_read_to_write(self, timeout: Optional[float] = None) -> None:
        """Attempts to upgrade from a shared read lock to an exclusive write.

        Raises:
            LockUpgradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._reads >= 1 and self._writes == 0:
            self._log_upgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.WRITE, timeout=timeout)
            self._reads = 0
            self._writes = 1
            self._log_upgraded(wait_time, nattempts)
        else:
            raise LockUpgradeError(self.path)

    def release_read(self, release_fn: ReleaseFnType = None) -> bool:
        """Releases a read lock.

        Arguments:
            release_fn: function to call *before* the last recursive lock (read or write) is
                released.

        If the last recursive lock will be released, then this will call release_fn and return its
        result (if provided), or return True (if release_fn was not provided).

        Otherwise, we are still nested inside some other lock, so do not call the release_fn and,
        return False.

        Does limited correctness checking: if a read lock is released when none are held, this
        will raise an assertion error.
        """
        assert self._reads > 0

        locktype = "READ LOCK"
        if self._reads == 1 and self._writes == 0:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            release_fn = release_fn or true_fn
            result = release_fn()

            self.backend.release()  # can raise LockError.
            self._reads = 0
            self._log_released(locktype)
            return bool(result)
        else:
            self._reads -= 1
            return False

    def release_write(self, release_fn: ReleaseFnType = None) -> bool:
        """Releases a write lock.

        Arguments:
            release_fn: function to call before the last recursive write is released.

        If the last recursive *write* lock will be released, then this will call release_fn and
        return its result (if provided), or return True (if release_fn was not provided).
        Otherwise, we are still nested inside some other write lock, so do not call the release_fn,
        and return False.

        Does limited correctness checking: if a read lock is released when none are held, this
        will raise an assertion error.
        """
        assert self._writes > 0
        release_fn = release_fn or true_fn

        locktype = "WRITE LOCK"
        if self._writes == 1:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            result = release_fn()

            if self._reads > 0:
                self._lock(LockType.READ)
            else:
                self.backend.release()  # can raise LockError.

            self._writes = 0
            self._log_released(locktype)
            return bool(result)
        else:
            self._writes -= 1
            return False

    def cleanup(self) -> None:
        if self._reads == 0 and self._writes == 0:
            self.backend.cleanup(self.path)
        else:
            raise LockError("Attempting to cleanup active lock.")

    def _get_counts_desc(self) -> str:
        return (
            "(reads {0}, writes {1})".format(self._reads, self._writes) if tty.is_verbose() else ""
        )

    def _log_acquired(self, locktype, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Acquired at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, "{0}{1}".format(desc, attempts_part)))

    def _log_acquiring(self, locktype) -> None:
        self._log_debug(self._status_msg(locktype, "Acquiring"), level=3)

    def _log_debug(self, *args, **kwargs) -> None:
        """Output lock debug messages."""
        kwargs["level"] = kwargs.get("level", 2)
        tty.debug(*args, **kwargs)

    def _log_downgraded(self, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Downgraded at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg("READ LOCK", "{0}{1}".format(desc, attempts_part)))

    def _log_downgrading(self) -> None:
        self._log_debug(self._status_msg("WRITE LOCK", "Downgrading"), level=3)

    def _log_released(self, locktype) -> None:
        now = datetime.now()
        desc = "Released at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, desc))

    def _log_releasing(self, locktype) -> None:
        self._log_debug(self._status_msg(locktype, "Releasing"), level=3)

    def _log_upgraded(self, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Upgraded at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg("WRITE LOCK", "{0}{1}".format(desc, attempts_part)))

    def _log_upgrading(self) -> None:
        self._log_debug(self._status_msg("READ LOCK", "Upgrading"), level=3)

    def _status_msg(self, locktype: str, status: str) -> str:
        status_desc = "[{0}] {1}".format(status, self._get_counts_desc())
        return "{0}{1.desc}: {1.path}[{1._start}:{1._length}] {2}".format(
            locktype, self, status_desc
        )


class LockTransaction:
    """Simple nested transaction context manager that uses a file lock.

    Arguments:
        lock: underlying lock for this transaction to be acquired on enter and released on exit
        acquire: function to be called after lock is acquired
        release: function to be called before release, with ``(exc_type, exc_value, traceback)``
        timeout: number of seconds to set for the timeout when acquiring the lock (default no
            timeout)
    """

    def __init__(
        self,
        lock: Lock,
        acquire: Optional[Callable[[], None]] = None,
        release: Optional[ExitFnType] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self._lock = lock
        self._timeout = timeout
        self._acquire_fn = acquire
        self._release_fn = release

    def __enter__(self):
        entered = self._enter()
        if entered and self._acquire_fn:
            try:
                return self._acquire_fn()
            except BaseException:
                # If __enter__ raises, Python never calls __exit__, so the lock _enter() just
                # acquired would otherwise leak.
                self._exit(None)
                raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        def release_fn():
            if self._release_fn is not None:
                return self._release_fn(exc_type, exc_value, traceback)

        return bool(self._exit(release_fn))

    def _enter(self) -> bool:
        raise NotImplementedError

    def _exit(self, release_fn: ReleaseFnType) -> bool:
        raise NotImplementedError


def check_lock_safety(path: str) -> None:
    """Do some extra checks to ensure disabling locks is safe.

    This will raise an error if ``path`` can is group- or world-writable
    AND the current user can write to the directory (i.e., if this user
    AND others could write to the path).

    This is intended to run on the Spack prefix, but can be run on any
    path for testing.
    """
    if os.access(path, os.W_OK):
        stat_result = os.stat(path)
        uid, gid = stat_result.st_uid, stat_result.st_gid
        mode = stat_result[stat.ST_MODE]

        writable = None
        if (mode & stat.S_IWGRP) and (uid != gid):
            # spack is group-writeable and the group is not the owner
            writable = "group"
        elif mode & stat.S_IWOTH:
            # spack is world-writeable
            writable = "world"

        if writable:
            msg = f"Refusing to disable locks: spack is {writable}-writable."
            long_msg = (
                f"Running a shared spack without locks is unsafe. You must "
                f"restrict permissions on {path} or enable locks."
            )
            raise spack.error.SpackError(msg, long_msg)


class ReadTransaction(LockTransaction):
    """LockTransaction context manager that does a read and releases it."""

    def _enter(self):
        return self._lock.acquire_read(self._timeout)

    def _exit(self, release_fn):
        return self._lock.release_read(release_fn)


class WriteTransaction(LockTransaction):
    """LockTransaction context manager that does a write and releases it."""

    def _enter(self):
        return self._lock.acquire_write(self._timeout)

    def _exit(self, release_fn):
        return self._lock.release_write(release_fn)


class TryReadTransaction(ReadTransaction):
    """Non-blocking ReadTransaction: yields True if the lock was acquired, and False if acquiring
    it would block, in which case the body must skip its work::

        with TryReadTransaction(lock, acquire=...) as acquired:
            if not acquired:
                return
            ...
    """

    def __init__(
        self,
        lock: Lock,
        acquire: Optional[Callable[[], None]] = None,
        release: Optional[ExitFnType] = None,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(lock, acquire=acquire, release=release, timeout=timeout)
        self._acquired = False

    def __enter__(self) -> bool:
        # The acquire function must only run on the outermost acquisition
        outermost = self._lock._reads == 0 and self._lock._writes == 0
        if not self._lock.try_acquire_read():
            return False
        self._acquired = True
        if outermost and self._acquire_fn:
            self._acquire_fn()
        return True

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if not self._acquired:
            return False
        return super().__exit__(exc_type, exc_value, traceback)


class TryWriteTransaction(WriteTransaction):
    """Non-blocking WriteTransaction: yields True if the lock was acquired, and False if acquiring
    it would block, in which case the body must skip its work::

        with TryWriteTransaction(lock, acquire=..., release=...) as acquired:
            if not acquired:
                return
            ...
    """

    def __init__(
        self,
        lock: Lock,
        acquire: Optional[Callable[[], None]] = None,
        release: Optional[ExitFnType] = None,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(lock, acquire=acquire, release=release, timeout=timeout)
        self._acquired = False

    def __enter__(self) -> bool:
        # The acquire function must only run on the outermost acquisition
        outermost = self._lock._writes == 0
        if not self._lock.try_acquire_write():
            return False
        self._acquired = True
        if outermost and self._acquire_fn:
            self._acquire_fn()
        return True

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if not self._acquired:
            return False
        return super().__exit__(exc_type, exc_value, traceback)


class LockError(Exception):
    """Raised for any errors related to locks."""


class LockDowngradeError(LockError):
    """Raised when unable to downgrade from a write to a read lock."""

    def __init__(self, path: str) -> None:
        msg = "Cannot downgrade lock from write to read on file: %s" % path
        super().__init__(msg)


class LockTimeoutError(LockError):
    """Raised when an attempt to acquire a lock times out."""

    def __init__(self, lock_type: int, path: str, time: float, attempts: int) -> None:
        lock_type_str = LockType.to_str(lock_type).lower()
        fmt = "Timed out waiting for a {} lock after {}.\n    Made {} {} on file: {}"
        super().__init__(
            fmt.format(
                lock_type_str,
                lang.pretty_seconds(time),
                attempts,
                "attempt" if attempts == 1 else "attempts",
                path,
            )
        )


class LockUpgradeError(LockError):
    """Raised when unable to upgrade from a read to a write lock."""

    def __init__(self, path: str) -> None:
        msg = "Cannot upgrade lock from read to write on file: %s" % path
        super().__init__(msg)


class LockPermissionError(LockError):
    """Raised when there are permission issues with a lock."""


class LockROFileError(LockPermissionError):
    """Tried to take an exclusive lock on a read-only file."""

    def __init__(self, path: str) -> None:
        msg = "Can't take write lock on read-only file: %s" % path
        super().__init__(msg)


class CantCreateLockError(LockPermissionError):
    """Attempt to create a lock in an unwritable location."""

    def __init__(self, path: str) -> None:
        msg = "cannot create lock '%s': " % path
        msg += "file does not exist and location is not writable"
        super().__init__(msg)
