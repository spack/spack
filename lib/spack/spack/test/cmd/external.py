# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import stat

import spack.spec
from spack.cmd.external import ExternalPackageEntry


@pytest.fixture()
def cmake_exe(tmpdir_factory):
    cmake_prefix = tmpdir_factory.mktemp('cmake-prefix')
    cmake_prefix.ensure('bin', dir=True)
    cmake_path = str(cmake_prefix.join('bin', 'cmake'))
    with open(cmake_path, 'w') as f:
        f.write("""\
#!/bin/bash

echo "cmake version 1.foo"
""")

    st = os.stat(cmake_path)
    os.chmod(cmake_path, st.st_mode | stat.S_IEXEC)

    system_path_to_exe = {cmake_path: 'cmake'}
    yield system_path_to_exe


def test_get_external_packages(cmake_exe):
    pkgs_to_check = [spack.repo.get('cmake')]
    pkg_to_entries = spack.cmd.external._get_external_packages(
        pkgs_to_check, cmake_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry.spec == spack.spec.Spec('cmake@1.foo')


def test_external_update_config(mutable_config):
    pkg_to_entries = {
        'cmake': [
            ExternalPackageEntry(spack.spec.Spec('cmake@1.foo'), '/x/y1/'),
            ExternalPackageEntry(spack.spec.Spec('cmake@2.foo'), '/x/y2/')
        ]
    }

    spack.cmd.external._update_pkg_config(pkg_to_entries)

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_paths_cfg = cmake_cfg['paths']

    assert cmake_paths_cfg['cmake@1.foo'] == '/x/y1/'
