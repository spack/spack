##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import pytest
import llnl.util.filesystem

import spack.cmd.compiler
import spack.compilers
import spack.spec
import spack.util.pattern
from spack.version import Version

test_version = '4.5-spacktest'


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


@pytest.mark.usefixtures('config', 'builtin_mock')
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
        assert new_compiler
        assert sum(1 for c in new_compiler if
                   c.version == Version(test_version)) > 0
