# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for Spack's wrapper module around spack.llnl.util.lock."""
import os
import pathlib

import pytest

import spack.error
import spack.util.lock as lk
from spack.llnl.util.filesystem import getuid, group_ids


def test_disable_locking(tmp_path: pathlib.Path):
    """Ensure that locks do no real locking when disabled."""
    lock_path = str(tmp_path / "lockfile")
    lock = lk.Lock(lock_path, enable=False)

    lock.acquire_read()
    assert not os.path.exists(lock_path)

    lock.acquire_write()
    assert not os.path.exists(lock_path)

    lock.release_write()
    assert not os.path.exists(lock_path)

    lock.release_read()
    assert not os.path.exists(lock_path)


# "Disable" mock_stage fixture to avoid subdir permissions issues on cleanup.
@pytest.mark.nomockstage
def test_lock_checks_user(tmp_path: pathlib.Path):
    """Ensure lock checks work with a self-owned, self-group repo."""
    uid = getuid()
    if uid not in group_ids():
        pytest.skip("user has no group with gid == uid")

    # self-owned, own group
    os.chown(tmp_path, uid, uid)

    # safe
    path = str(tmp_path)
    tmp_path.chmod(0o744)
    lk.check_lock_safety(path)

    # safe
    tmp_path.chmod(0o774)
    lk.check_lock_safety(path)

    # unsafe
    tmp_path.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmp_path.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmp_path.chmod(0o477)
    lk.check_lock_safety(path)


# "Disable" mock_stage fixture to avoid subdir permissions issues on cleanup.
@pytest.mark.nomockstage
def test_lock_checks_group(tmp_path: pathlib.Path):
    """Ensure lock checks work with a self-owned, non-self-group repo."""
    uid = getuid()
    gid = next((g for g in group_ids() if g != uid), None)
    if not gid:
        pytest.skip("user has no group with gid != uid")
        return

    # self-owned, another group
    os.chown(tmp_path, uid, gid)

    # safe
    path = str(tmp_path)
    tmp_path.chmod(0o744)
    lk.check_lock_safety(path)

    # unsafe
    tmp_path.chmod(0o774)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # unsafe
    tmp_path.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmp_path.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmp_path.chmod(0o477)
    lk.check_lock_safety(path)
