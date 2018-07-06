# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest
import llnl.util.filesystem
import llnl.util.multiproc

import spack.cmd.compiler
import spack.compilers
import spack.spec
import spack.util.pattern
from spack.version import Version

test_version = '4.5-spacktest'
test_multiple_version = '4.8-spacktest'
test_pgi_version = '0.0'
test_pgi_version_string = 'pgi 0.0-0 pgi target on pgispacktest'


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


@pytest.fixture()
def mock_two_compiler_dirs(tmpdir):
    """Return two directory containing a fake, but detectable compiler,
    with the same compiler spec."""

    tmpdir.ensure('compiler1/bin', dir=True)
    tmpdir1 = tmpdir.join('compiler1')
    bin_dir1 = tmpdir1.join('bin')

    gcc_path1 = bin_dir1.join('gcc')
    gxx_path1 = bin_dir1.join('g++')
    gfortran_path1 = bin_dir1.join('gfortran')

    tmpdir.ensure('compiler2/bin', dir=True)
    tmpdir2 = tmpdir.join('compiler2')
    bin_dir2 = tmpdir2.join('bin')

    gcc_path2 = bin_dir2.join('gcc')
    gxx_path2 = bin_dir2.join('g++')
    gfortran_path2 = bin_dir2.join('gfortran')

    gcc_path1.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % test_multiple_version)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(gcc_path1))
    gcc_path1.copy(gxx_path1, mode=True)
    gcc_path1.copy(gfortran_path1, mode=True)

    gcc_path1.copy(gcc_path2, mode=True)
    gcc_path1.copy(gxx_path2, mode=True)
    gcc_path1.copy(gfortran_path2, mode=True)

    return [str(tmpdir1), str(tmpdir2)]


@pytest.fixture()
def mock_pgi_dir(tmpdir):
    """Return a directory containing a fake, but detectable pgi compiler,
    with both old (pgf77, pgf90) and new (pgfortran) names."""

    tmpdir.ensure('bin', dir=True)
    bin_dir = tmpdir.join('bin')

    pgcc_path = bin_dir.join('pgcc')
    pgxx_path = bin_dir.join('pg++')
    pgfortran_path = bin_dir.join('pgfortran')
    pgf77_path = bin_dir.join('pgf77')
    pgf90_path = bin_dir.join('pgf90')

    pgcc_path.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -V ]; then
        echo '%s'
    fi
done
""" % test_pgi_version_string)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(pgcc_path))
    pgcc_path.copy(pgxx_path, mode=True)
    pgcc_path.copy(pgfortran_path, mode=True)
    pgcc_path.copy(pgf77_path, mode=True)
    pgcc_path.copy(pgf90_path, mode=True)

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

    def test_compiler_add(self, mock_compiler_dir, monkeypatch):
        # This test randomly stall on Travis when spawning processes
        # in Python 2.6 unit tests
        if sys.version_info < (3, 0, 0):
            monkeypatch.setattr(llnl.util.multiproc, 'parmap', map)

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

    def test_compiler_add_multiple_in_path(self, mock_two_compiler_dirs):
        # Compilers available by default.
        old_compilers = set(spack.compilers.all_compiler_specs())

        args = spack.util.pattern.Bunch(
            all=None,
            compiler_spec=None,
            add_paths=mock_two_compiler_dirs,
            scope=None
        )
        spack.cmd.compiler.compiler_find(args)

        # Ensure new compiler is from the first path passed
        new_all_compilers = set(spack.compilers.all_compiler_specs())
        new_compilers = new_all_compilers - old_compilers

        new_comp = spack.compilers.compilers_for_spec('gcc@%s'
                                                      % test_multiple_version)
        assert mock_two_compiler_dirs[0] in new_comp[0].cc
        assert any(c.version == Version(test_multiple_version)
                   for c in new_compilers)

        # sorting to avoid gcc@4.8 removing gcc@4.8-spacktest and causing error
        for compiler in sorted(new_compilers, reverse=True):
            rm_args = spack.util.pattern.Bunch(
                all=True, compiler_spec=compiler, add_paths=[], scope=None
            )
            spack.cmd.compiler.compiler_remove(rm_args)

    def test_compiler_add_multiple_names(self, mock_pgi_dir):
        old_compilers = set(spack.compilers.all_compiler_specs())

        args = spack.util.pattern.Bunch(
            all=None,
            compiler_spec=None,
            add_paths=[mock_pgi_dir],
            scope=None
        )
        spack.cmd.compiler.compiler_find(args)

        # Ensure new compiler is in there and has newest pgi names
        new_compilers = set(spack.compilers.all_compiler_specs())
        n_compiler = new_compilers - old_compilers

        new_comp = spack.compilers.compilers_for_spec('pgi@%s'
                                                      % test_pgi_version)
        assert 'pgfortran' in new_comp[0].f77
        assert 'pgfortran' in new_comp[0].fc
        assert any(c.version == Version(test_pgi_version) for c in n_compiler)

        for compiler in n_compiler:
            rm_args = spack.util.pattern.Bunch(
                all=True, compiler_spec=compiler, add_paths=[], scope=None
            )
            spack.cmd.compiler.compiler_remove(rm_args)
