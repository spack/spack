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
"""Tests for Spack's wrapper module around llnl.util.lock."""
import os

import pytest

from llnl.util.filesystem import group_ids

import spack.config
import spack.util.lock as lk


def test_disable_locking(tmpdir):
    """Ensure that locks do no real locking when disabled."""
    lock_path = str(tmpdir.join('lockfile'))

    old_value = spack.config.get('config:locks')

    with spack.config.override('config:locks', False):
        lock = lk.Lock(lock_path)

        lock.acquire_read()
        assert not os.path.exists(lock_path)

        lock.acquire_write()
        assert not os.path.exists(lock_path)

        lock.release_write()
        assert not os.path.exists(lock_path)

        lock.release_read()
        assert not os.path.exists(lock_path)

    assert old_value == spack.config.get('config:locks')


def test_lock_checks_user(tmpdir):
    """Ensure lock checks work with a self-owned, self-group repo."""
    uid = os.getuid()
    if uid not in group_ids():
        pytest.skip("user has no group with gid == uid")

    # self-owned, own group
    tmpdir.chown(uid, uid)

    # safe
    path = str(tmpdir)
    tmpdir.chmod(0o744)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o774)
    lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o477)
    lk.check_lock_safety(path)


def test_lock_checks_group(tmpdir):
    """Ensure lock checks work with a self-owned, non-self-group repo."""
    uid = os.getuid()
    gid = next((g for g in group_ids() if g != uid), None)
    if not gid:
        pytest.skip("user has no group with gid != uid")

    # self-owned, another group
    tmpdir.chown(uid, gid)

    # safe
    path = str(tmpdir)
    tmpdir.chmod(0o744)
    lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o774)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o477)
    lk.check_lock_safety(path)
