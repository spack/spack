# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""fcntl-based lock backend for POSIX systems, and the concrete ``LockType`` that supplies its
native flag values.
"""

import sys

if sys.platform == "win32":
    # Also lets mypy skip this module when run on Windows.
    raise ImportError("spack.util.lock_posix can only be imported on POSIX platforms")

import errno
import fcntl
import os
import stat

import spack.error
from spack.util import tty
from spack.util.lock_common import GenericLockBackend
from spack.util.lock_common import LockType as _LockType


class LockType(_LockType):
    LOCK_SH = fcntl.LOCK_SH
    LOCK_EX = fcntl.LOCK_EX
    LOCK_NB = fcntl.LOCK_NB
    LOCK_UN = fcntl.LOCK_UN

    @staticmethod
    def to_module(tid):
        lock = LockType.LOCK_SH
        if tid == LockType.WRITE:
            lock = LockType.LOCK_EX
        return lock


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

        except OSError as e:
            # EAGAIN and EACCES == locked by another process (so try again)
            if e.errno not in (errno.EAGAIN, errno.EACCES):
                raise

        return False

    def release(self) -> None:
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may be masquerading as write
        locks, but this removes either.
        """
        assert self._file_ref is not None, "cannot unlock without the file being set"
        fcntl.lockf(
            self._file_ref.fh.fileno(), LockType.LOCK_UN, self._length, self._start, os.SEEK_SET
        )


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
