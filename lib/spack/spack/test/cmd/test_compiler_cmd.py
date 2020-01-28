# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import llnl.util.filesystem

import spack.cmd.compiler
import spack.compilers
import spack.spec
import spack.util.pattern
from spack.version import Version

test_version = '4.5.3'


@pytest.fixture()
def mock_compiler_dir(tmpdir):
    """Return a directory containing a fake, but detectable compiler."""

    tmpdir.ensure('bin', dir=True)
    bin_dir = tmpdir.join('bin')

    gcc_path = bin_dir.join('gcc')
    gxx_path = bin_dir.join('g++')
    gfortran_path = bin_dir.join('gfortran')

    gcc_path.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % test_version)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(gcc_path))
    gcc_path.copy(gxx_path, mode=True)
    gcc_path.copy(gfortran_path, mode=True)

    return str(tmpdir)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestCompilerCommand(object):

    def test_compiler_remove(self):
        args = spack.util.pattern.Bunch(
            all=True, compiler_spec='gcc@4.5.0', add_paths=[], scope=None
        )
        spack.cmd.compiler.compiler_remove(args)
        compilers = spack.compilers.all_compiler_specs()
        assert spack.spec.CompilerSpec("gcc@4.5.0") not in compilers

    def test_compiler_add(self, mock_compiler_dir):
        # Compilers available by default.
        old_compilers = set(spack.compilers.all_compiler_specs())

        args = spack.util.pattern.Bunch(
            all=None,
            compiler_spec=None,
            add_paths=[mock_compiler_dir],
            scope=None
        )
        spack.cmd.compiler.compiler_find(args)

        # Ensure new compiler is in there
        new_compilers = set(spack.compilers.all_compiler_specs())
        new_compiler = new_compilers - old_compilers
        assert any(c.version == Version(test_version) for c in new_compiler)
