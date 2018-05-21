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
"""Wrapper for ``llnl.util.lock`` allows locking to be enabled/disabled."""
import os
import stat

import llnl.util.lock
from llnl.util.lock import *  # noqa

import spack.config
import spack.error
import spack.paths


class Lock(llnl.util.lock.Lock):
    """Lock that can be disabled.

    This overrides the ``_lock()`` and ``_unlock()`` methods from
    ``llnl.util.lock`` so that all the lock API calls will succeed, but
    the actual locking mechanism can be disabled via ``_enable_locks``.
    """
    def __init__(self, *args, **kwargs):
        super(Lock, self).__init__(*args, **kwargs)
        self._enable = spack.config.get('config:locks', True)

    def _lock(self, op, timeout=0):
        if self._enable:
            super(Lock, self)._lock(op, timeout)

    def _unlock(self):
        """Unlock call that always succeeds."""
        if self._enable:
            super(Lock, self)._unlock()

    def _debug(self, *args):
        if self._enable:
            super(Lock, self)._debug(*args)


def check_lock_safety(path):
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
            writable = 'group'
        elif (mode & stat.S_IWOTH):
            # spack is world-writeable
            writable = 'world'

        if writable:
            msg = "Refusing to disable locks: spack is {0}-writable.".format(
                writable)
            long_msg = (
                "Running a shared spack without locks is unsafe. You must "
                "restrict permissions on {0} or enable locks.").format(path)
            raise spack.error.SpackError(msg, long_msg)
