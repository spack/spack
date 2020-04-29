# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import stat

import spack.spec


@pytest.fixture()
def cmake_exe(tmpdir):
    cmake_path = str(tmpdir.join('cmake'))
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
