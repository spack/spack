# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Re-exports of :mod:`spack.llnl.util.lock` along with :func:`check_lock_safety`."""

import os
import stat

import spack.error
from spack.llnl.util.lock import (
    Lock,
    LockDowngradeError,
    LockError,
    LockTimeoutError,
    LockUpgradeError,
    ReadTransaction,
    WriteTransaction,
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


__all__ = [
    "check_lock_safety",
    "Lock",
    "LockDowngradeError",
    "LockError",
    "LockTimeoutError",
    "LockUpgradeError",
    "ReadTransaction",
    "WriteTransaction",
]
