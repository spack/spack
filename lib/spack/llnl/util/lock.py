##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import fcntl
import errno
import time
import socket

import llnl.util.tty as tty


__all__ = ['Lock', 'LockTransaction', 'WriteTransaction', 'ReadTransaction',
           'LockError', 'LockTimeoutError',
           'LockPermissionError', 'LockROFileError', 'CantCreateLockError']


# Default timeout in seconds, after which locks will raise exceptions.
_default_timeout = 60

# Sleep time per iteration in spin loop (in seconds)
_sleep_time = 1e-5


class Lock(object):
    """This is an implementation of a filesystem lock using Python's lockf.

    In Python, ``lockf`` actually calls ``fcntl``, so this should work with
    any filesystem implementation that supports locking through the fcntl
    calls.  This includes distributed filesystems like Lustre (when flock
    is enabled) and recent NFS versions.
    """

    def __init__(self, path, start=0, length=0, debug=False):
        """Construct a new lock on the file at ``path``.

        By default, the lock applies to the whole file.  Optionally,
        caller can specify a byte range beginning ``start`` bytes from
        the start of the file and extending ``length`` bytes from there.

        This exposes a subset of fcntl locking functionality.  It does
        not currently expose the ``whence`` parameter -- ``whence`` is
        always ``os.SEEK_SET`` and ``start`` is always evaluated from the
        beginning of the file.
        """
        self.path = path
        self._file = None
        self._reads = 0
        self._writes = 0

        # byte range parameters
        self._start = start
        self._length = length

        # enable debug mode
        self.debug = debug

        # PID and host of lock holder (only used in debug mode)
        self.pid = self.old_pid = None
        self.host = self.old_host = None

    def _lock(self, op, timeout=_default_timeout):
        """This takes a lock using POSIX locks (``fcntl.lockf``).

        The lock is implemented as a spin lock using a nonblocking call
        to ``lockf()``.

        On acquiring an exclusive lock, the lock writes this process's
        pid and host to the lock file, in case the holding process needs
        to be killed later.

        If the lock times out, it raises a ``LockError``.
        """
        assert op in (fcntl.LOCK_SH, fcntl.LOCK_EX)

        start_time = time.time()
        while (time.time() - start_time) < timeout:
            # Create file and parent directories if they don't exist.
            if self._file is None:
                parent = self._ensure_parent_directory()

                # Open writable files as 'r+' so we can upgrade to write later
                os_mode, fd_mode = (os.O_RDWR | os.O_CREAT), 'r+'
                if os.path.exists(self.path):
                    if not os.access(self.path, os.W_OK):
                        if op == fcntl.LOCK_SH:
                            # can still lock read-only files if we open 'r'
                            os_mode, fd_mode = os.O_RDONLY, 'r'
                        else:
                            raise LockROFileError(self.path)

                elif not os.access(parent, os.W_OK):
                    raise CantCreateLockError(self.path)

                fd = os.open(self.path, os_mode)
                self._file = os.fdopen(fd, fd_mode)

            elif op == fcntl.LOCK_EX and self._file.mode == 'r':
                # Attempt to upgrade to write lock w/a read-only file.
                # If the file were writable, we'd have opened it 'r+'
                raise LockROFileError(self.path)

            try:
                # Try to get the lock (will raise if not available.)
                fcntl.lockf(self._file, op | fcntl.LOCK_NB,
                            self._length, self._start, os.SEEK_SET)

                # help for debugging distributed locking
                if self.debug:
                    # All locks read the owner PID and host
                    self._read_debug_data()

                    # Exclusive locks write their PID/host
                    if op == fcntl.LOCK_EX:
                        self._write_debug_data()

                return

            except IOError as e:
                if e.errno in (errno.EAGAIN, errno.EACCES):
                    # EAGAIN and EACCES == locked by another process
                    pass
                else:
                    raise

            time.sleep(_sleep_time)

        raise LockTimeoutError("Timed out waiting for lock.")

    def _ensure_parent_directory(self):
        parent = os.path.dirname(self.path)

        # relative paths to lockfiles in the current directory have no parent
        if not parent:
            return '.'

        try:
            os.makedirs(parent)
        except OSError as e:
            # makedirs can fail when diretory already exists.
            if not (e.errno == errno.EEXIST and os.path.isdir(parent) or
                    e.errno == errno.EISDIR):
                raise
        return parent

    def _read_debug_data(self):
        """Read PID and host data out of the file if it is there."""
        self.old_pid = self.pid
        self.old_host = self.host

        line = self._file.read()
        if line:
            pid, host = line.strip().split(',')
            _, _, self.pid = pid.rpartition('=')
            _, _, self.host = host.rpartition('=')
            self.pid = int(self.pid)

    def _write_debug_data(self):
        """Write PID and host data to the file, recording old values."""
        self.old_pid = self.pid
        self.old_host = self.host

        self.pid = os.getpid()
        self.host = socket.getfqdn()

        # write pid, host to disk to sync over FS
        self._file.seek(0)
        self._file.write("pid=%s,host=%s" % (self.pid, self.host))
        self._file.truncate()
        self._file.flush()
        os.fsync(self._file.fileno())

    def _unlock(self):
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may
        be masquerading as write locks, but this removes either.

        """
        fcntl.lockf(self._file, fcntl.LOCK_UN,
                    self._length, self._start, os.SEEK_SET)
        self._file.close()
        self._file = None

    def acquire_read(self, timeout=_default_timeout):
        """Acquires a recursive, shared lock for reading.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        if self._reads == 0 and self._writes == 0:
            self._debug(
                'READ LOCK: {0.path}[{0._start}:{0._length}] [Acquiring]'
                .format(self))
            self._lock(fcntl.LOCK_SH, timeout=timeout)   # can raise LockError.
            self._debug(
                'READ LOCK: {0.path}[{0._start}:{0._length}] [Acquired]'
                .format(self))
            self._reads += 1
            return True
        else:
            self._reads += 1
            return False

    def acquire_write(self, timeout=_default_timeout):
        """Acquires a recursive, exclusive lock for writing.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        if self._writes == 0:
            self._debug(
                'WRITE LOCK: {0.path}[{0._start}:{0._length}] [Acquiring]'
                .format(self))
            self._lock(fcntl.LOCK_EX, timeout=timeout)   # can raise LockError.
            self._debug(
                'WRITE LOCK: {0.path}[{0._start}:{0._length}] [Acquired]'
                .format(self))
            self._writes += 1
            return True
        else:
            self._writes += 1
            return False

    def release_read(self):
        """Releases a read lock.

        Returns True if the last recursive lock was released, False if
        there are still outstanding locks.

        Does limited correctness checking: if a read lock is released
        when none are held, this will raise an assertion error.

        """
        assert self._reads > 0

        if self._reads == 1 and self._writes == 0:
            self._debug(
                'READ LOCK: {0.path}[{0._start}:{0._length}] [Released]'
                .format(self))
            self._unlock()      # can raise LockError.
            self._reads -= 1
            return True
        else:
            self._reads -= 1
            return False

    def release_write(self):
        """Releases a write lock.

        Returns True if the last recursive lock was released, False if
        there are still outstanding locks.

        Does limited correctness checking: if a read lock is released
        when none are held, this will raise an assertion error.

        """
        assert self._writes > 0

        if self._writes == 1 and self._reads == 0:
            self._debug(
                'WRITE LOCK: {0.path}[{0._start}:{0._length}] [Released]'
                .format(self))
            self._unlock()      # can raise LockError.
            self._writes -= 1
            return True
        else:
            self._writes -= 1
            return False

    def _debug(self, *args):
        tty.debug(*args)


class LockTransaction(object):
    """Simple nested transaction context manager that uses a file lock.

    This class can trigger actions when the lock is acquired for the
    first time and released for the last.

    If the ``acquire_fn`` returns a value, it is used as the return value for
    ``__enter__``, allowing it to be passed as the ``as`` argument of a
    ``with`` statement.

    If ``acquire_fn`` returns a context manager, *its* ``__enter__`` function
    will be called in ``__enter__`` after ``acquire_fn``, and its ``__exit__``
    funciton will be called before ``release_fn`` in ``__exit__``, allowing you
    to nest a context manager to be used along with the lock.

    Timeout for lock is customizable.

    """

    def __init__(self, lock, acquire_fn=None, release_fn=None,
                 timeout=_default_timeout):
        self._lock = lock
        self._timeout = timeout
        self._acquire_fn = acquire_fn
        self._release_fn = release_fn
        self._as = None

    def __enter__(self):
        if self._enter() and self._acquire_fn:
            self._as = self._acquire_fn()
            if hasattr(self._as, '__enter__'):
                return self._as.__enter__()
            else:
                return self._as

    def __exit__(self, type, value, traceback):
        suppress = False
        if self._exit():
            if self._as and hasattr(self._as, '__exit__'):
                if self._as.__exit__(type, value, traceback):
                    suppress = True
            if self._release_fn:
                if self._release_fn(type, value, traceback):
                    suppress = True
        return suppress


class ReadTransaction(LockTransaction):
    """LockTransaction context manager that does a read and releases it."""
    def _enter(self):
        return self._lock.acquire_read(self._timeout)

    def _exit(self):
        return self._lock.release_read()


class WriteTransaction(LockTransaction):
    """LockTransaction context manager that does a write and releases it."""
    def _enter(self):
        return self._lock.acquire_write(self._timeout)

    def _exit(self):
        return self._lock.release_write()


class LockError(Exception):
    """Raised for any errors related to locks."""


class LockTimeoutError(LockError):
    """Raised when an attempt to acquire a lock times out."""


class LockPermissionError(LockError):
    """Raised when there are permission issues with a lock."""


class LockROFileError(LockPermissionError):
    """Tried to take an exclusive lock on a read-only file."""
    def __init__(self, path):
        msg = "Can't take write lock on read-only file: %s" % path
        super(LockROFileError, self).__init__(msg)


class CantCreateLockError(LockPermissionError):
    """Attempt to create a lock in an unwritable location."""
    def __init__(self, path):
        msg = "cannot create lock '%s': " % path
        msg += "file does not exist and location is not writable"
        super(LockError, self).__init__(msg)
