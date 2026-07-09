# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat
import sys
import time
from datetime import datetime
from types import TracebackType
from typing import Callable, Generator, Optional, Tuple, Type  # novm

import spack.error
from spack.util import lang, tty
from spack.util.lock_common import (
    FILE_TRACKER,
    CantCreateLockError,
    GenericLockBackend,
    LockError,
    LockPermissionError,
    LockROFileError,
)
from spack.util.string import plural


if sys.platform == "win32":
    from spack.util.lock_windows import LockType, WindowsBackend
else:
    from spack.util.lock_posix import LockType, PosixBackend


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
    "DummyBackend",
    "FILE_TRACKER",
]

WHOLE_FILE_RANGE = 0xFFFFFFFF if sys.platform == "win32" else 0


ExitFnType = Callable[
    [Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]],
    Optional[bool],
]
ReleaseFnType = Optional[Callable[[], Optional[bool]]]


def true_fn() -> bool:
    """A function that always returns True."""
    return True


def _attempts_str(wait_time, nattempts):
    # Don't print anything if we succeeded on the first try
    if nattempts <= 1:
        return ""

    attempts = plural(nattempts, "attempt")
    return " after {} and {}".format(lang.pretty_seconds(wait_time), attempts)


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


#: Every backend derives from GenericLockBackend, and ``Lock`` only ever calls the methods
#: defined there -- using the base class here (rather than a Union of concrete backends) avoids
#: needing to reference the Windows-only ``WindowsBackend`` outside of a literal
#: ``sys.platform``-guarded import, which is what lets type checkers running on non-Windows
#: platforms (e.g. Read the Docs) skip ``spack.util.lock_windows`` entirely.
BackendType = GenericLockBackend


def platform_lock_backend(path, start, length, debug) -> BackendType:
    """Per platform dispatch for lock backend implementation"""
    if sys.platform == "win32":
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
        if sys.platform == "win32":
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
