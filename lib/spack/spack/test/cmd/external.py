# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import stat

import spack
from spack.spec import Spec
from spack.cmd.external import ExternalPackageEntry


@pytest.fixture()
def create_cmake_exe(tmpdir_factory):
    def _create_cmake_exe(version):
        cmake_prefix = tmpdir_factory.mktemp('cmake-prefix')
        cmake_prefix.ensure('bin', dir=True)
        cmake_path = str(cmake_prefix.join('bin', 'cmake'))
        with open(cmake_path, 'w') as f:
            f.write("""\
#!/bin/bash

echo "cmake version {version}"
""".format(version=version))

        st = os.stat(cmake_path)
        os.chmod(cmake_path, st.st_mode | stat.S_IEXEC)
        return cmake_path

    yield _create_cmake_exe


def test_find_external_single_package(create_cmake_exe):
    pkgs_to_check = [spack.repo.get('cmake')]

    cmake_path = create_cmake_exe("1.foo")
    system_path_to_exe = {cmake_path: 'cmake'}

    pkg_to_entries = spack.cmd.external._get_external_packages(
        pkgs_to_check, system_path_to_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry.spec == Spec('cmake@1.foo')


def test_find_external_two_instances_same_package(create_cmake_exe):
    pkgs_to_check = [spack.repo.get('cmake')]

    cmake_path1 = create_cmake_exe("1.foo")
    cmake_path2 = create_cmake_exe("3.17.2")
    system_path_to_exe = {
        cmake_path1: 'cmake',
        cmake_path2: 'cmake'}

    pkg_to_entries = spack.cmd.external._get_external_packages(
        pkgs_to_check, system_path_to_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    collected_specs = set(entry.spec for entry in entries)
    assert set([Spec('cmake@1.foo'), Spec('cmake@3.17.2')]) == collected_specs


def test_find_external_update_config(mutable_config):
    pkg_to_entries = {
        'cmake': [
            ExternalPackageEntry(Spec('cmake@1.foo'), '/x/y1/'),
            ExternalPackageEntry(Spec('cmake@3.17.2'), '/x/y2/'),
        ]
    }

    spack.cmd.external._update_pkg_config(pkg_to_entries)

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_paths_cfg = cmake_cfg['paths']

    assert cmake_paths_cfg['cmake@1.foo'] == '/x/y1/'
    assert cmake_paths_cfg['cmake@3.17.2'] == '/x/y2/'
