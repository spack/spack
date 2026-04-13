# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import os
import socket
import sys
import time
from datetime import datetime
from types import TracebackType
from typing import IO, Callable, Dict, Generator, Optional, Tuple, Type

from spack.llnl.util import lang, tty

from ..string import plural

if sys.platform != "win32":
    import fcntl


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
]


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
    the next lock operation can skip re-opening the file. ``Lock._ensure_valid_handle``
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


def _attempts_str(wait_time, nattempts):
    # Don't print anything if we succeeded on the first try
    if nattempts <= 1:
        return ""

    attempts = plural(nattempts, "attempt")
    return " after {} and {}".format(lang.pretty_seconds(wait_time), attempts)


class LockType:
    READ = 0
    WRITE = 1

    @staticmethod
    def to_str(tid):
        ret = "READ"
        if tid == LockType.WRITE:
            ret = "WRITE"
        return ret

    @staticmethod
    def to_module(tid):
        lock = fcntl.LOCK_SH
        if tid == LockType.WRITE:
            lock = fcntl.LOCK_EX
        return lock

    @staticmethod
    def is_valid(op: int) -> bool:
        return op == LockType.READ or op == LockType.WRITE


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
        """
        self.path = path
        self._reads = 0
        self._writes = 0
        self._file_ref: Optional[OpenFile] = None
        self._cached_key: Optional[DevIno] = None

        # byte range parameters
        self._start = start
        self._length = length

        # enable debug mode
        self.debug = debug

        # optional debug description
        self.desc = f" ({desc})" if desc else ""

        # If the user doesn't set a default timeout, or if they choose
        # None, 0, etc. then lock attempts will not time out (unless the
        # user sets a timeout for each attempt)
        self.default_timeout = default_timeout or None

        # PID and host of lock holder (only used in debug mode)
        self.pid: Optional[int] = None
        self.old_pid: Optional[int] = None
        self.host: Optional[str] = None
        self.old_host: Optional[str] = None

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
        """Don't include file handles or counts in pickled state."""
        state = self.__dict__.copy()
        del state["_file_ref"]
        del state["_reads"]
        del state["_writes"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._file_ref = None
        self._reads = 0
        self._writes = 0

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

        fh = self._ensure_valid_handle()

        if LockType.to_module(op) == fcntl.LOCK_EX and fh.mode == "rb":
            # Attempt to upgrade to write lock w/a read-only file.
            # If the file were writable, we'd have opened it rb+
            raise LockROFileError(self.path)

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
            if self._poll_lock(op):
                return time.monotonic() - start_time, num_attempts
            if time.monotonic() >= end_time:
                break
            time.sleep(next(poll_intervals))
            num_attempts += 1

        raise LockTimeoutError(op, self.path, time.monotonic() - start_time, num_attempts)

    def _poll_lock(self, op: int) -> bool:
        """Attempt to acquire the lock in a non-blocking manner. Return whether
        the locking attempt succeeds
        """
        assert self._file_ref is not None, "cannot poll a lock without the file being set"
        fh = self._file_ref.fh.fileno()
        module_op = LockType.to_module(op)
        try:
            # Try to get the lock (will raise if not available.)
            fcntl.lockf(fh, module_op | fcntl.LOCK_NB, self._length, self._start, os.SEEK_SET)

            # help for debugging distributed locking
            if self.debug:
                # All locks read the owner PID and host
                self._read_log_debug_data()
                self._log_debug(
                    "{0} locked {1} [{2}:{3}] (owner={4})".format(
                        LockType.to_str(op), self.path, self._start, self._length, self.pid
                    )
                )

                # Exclusive locks write their PID/host
                if module_op == fcntl.LOCK_EX:
                    self._write_log_debug_data()

            return True

        except OSError as e:
            # EAGAIN and EACCES == locked by another process (so try again)
            if e.errno not in (errno.EAGAIN, errno.EACCES):
                raise

        return False

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

    def _unlock(self) -> None:
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may be masquerading as write
        locks, but this removes either.
        """
        assert self._file_ref is not None, "cannot unlock without the file being set"
        fcntl.lockf(
            self._file_ref.fh.fileno(), fcntl.LOCK_UN, self._length, self._start, os.SEEK_SET
        )
        self._reads = 0
        self._writes = 0

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
        if we hold an exclusive lock so we don't accidentally downgrade it."""
        if self._writes > 0:
            op = LockType.WRITE
        elif self._reads > 0:
            op = LockType.READ
        else:
            return
        self._ensure_valid_handle()
        if not self._poll_lock(op):
            raise LockTimeoutError(op, self.path, time=0, attempts=1)

    def try_acquire_read(self) -> bool:
        """Non-blocking attempt to acquire a shared read lock.

        Returns True if the lock was acquired, False if it would block.
        """
        if self._reads == 0 and self._writes == 0:
            self._ensure_valid_handle()
            if not self._poll_lock(LockType.READ):
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
        """
        if self._writes == 0:
            fh = self._ensure_valid_handle()
            if LockType.to_module(LockType.WRITE) == fcntl.LOCK_EX and fh.mode == "rb":
                raise LockROFileError(self.path)
            if not self._poll_lock(LockType.WRITE):
                return False
            self._writes += 1
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

        if self._reads == 1 and self._writes == 0:
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

            self._unlock()  # can raise LockError.
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
                self._unlock()  # can raise LockError.

            self._writes = 0
            self._log_released(locktype)
            return bool(result)
        else:
            self._writes -= 1
            return False

    def cleanup(self) -> None:
        if self._reads == 0 and self._writes == 0:
            os.unlink(self.path)
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
        if self._enter() and self._acquire_fn:
            return self._acquire_fn()

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
