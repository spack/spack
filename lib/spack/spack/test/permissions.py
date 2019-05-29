# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest
import stat

from spack.hooks.permissions_setters import (
    chmod_real_entries, InvalidPermissionsError
)
import llnl.util.filesystem as fs


def test_chmod_real_entries_ignores_suid_sgid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX
    os.chmod(path, mode)
    mode = os.stat(path).st_mode  # adds a high bit we aren't concerned with

    perms = stat.S_IRWXU
    chmod_real_entries(path, perms)

    assert os.stat(path).st_mode == mode | perms & ~stat.S_IXUSR


def test_chmod_rejects_group_writable_suid(tmpdir):
    path = str(tmpdir.join('file').ensure())
    mode = stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX
    fs.chmod_x(path, mode)

    perms = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
    with pytest.raises(InvalidPermissionsError):
        chmod_real_entries(path, perms)
