# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Platform-neutral plumbing shared by ``spack.util.lock``'s backends: the open-file tracker,
the ``LockType`` base, ``GenericLockBackend``, and the handful of lock exceptions backend code
itself needs to raise.
"""

import errno
import os
import socket
from typing import IO, Dict, Optional, Tuple

DevIno = Tuple[int, int]  # (st_dev, st_ino) from os.stat_result


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


class LockType:
    """Platform-neutral lock operation identifiers.
    """

    READ = 0
    WRITE = 1

    @staticmethod
    def to_str(tid):
        ret = "READ"
        if tid == LockType.WRITE:
            ret = "WRITE"
        return ret

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

        if op == LockType.WRITE and fh.mode == "rb":
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


class LockError(Exception):
    """Raised for any errors related to locks."""


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
