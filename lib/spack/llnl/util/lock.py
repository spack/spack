##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import fcntl
import errno
import time
import socket

# Default timeout in seconds, after which locks will raise exceptions.
_default_timeout = 60

# Sleep time per iteration in spin loop (in seconds)
_sleep_time = 1e-5


class Lock(object):
    def __init__(self,file_path):
        self._file_path = file_path
        self._fd = None
        self._reads = 0
        self._writes = 0


    def _lock(self, op, timeout):
        """This takes a lock using POSIX locks (``fnctl.lockf``).

        The lock is implemented as a spin lock using a nonblocking
        call to lockf().

        On acquiring an exclusive lock, the lock writes this process's
        pid and host to the lock file, in case the holding process
        needs to be killed later.

        If the lock times out, it raises a ``LockError``.
        """
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            try:
                if self._fd is None:
                    self._fd = os.open(self._file_path, os.O_RDWR)

                fcntl.lockf(self._fd, op | fcntl.LOCK_NB)
                if op == fcntl.LOCK_EX:
                    os.write(self._fd, "pid=%s,host=%s" % (os.getpid(), socket.getfqdn()))
                return

            except IOError as error:
                if error.errno == errno.EAGAIN or error.errno == errno.EACCES:
                    pass
                else:
                    raise
            time.sleep(_sleep_time)

        raise LockError("Timed out waiting for lock.")


    def _unlock(self):
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may
        be masquerading as write locks, but this removes either.

        """
        fcntl.lockf(self._fd,fcntl.LOCK_UN)
        os.close(self._fd)
        self._fd = None


    def acquire_read(self, timeout=_default_timeout):
        """Acquires a recursive, shared lock for reading.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        if self._reads == 0 and self._writes == 0:
            self._lock(fcntl.LOCK_SH, timeout)   # can raise LockError.
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
            self._lock(fcntl.LOCK_EX, timeout)   # can raise LockError.
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
            self._unlock()      # can raise LockError.
            self._writes -= 1
            return True
        else:
            self._writes -= 1
            return False


class LockError(Exception):
    """Raised when an attempt to acquire a lock times out."""
    pass
