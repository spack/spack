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
import pytest
import os

import spack.spec
import spack.repo
import spack.build_environment


@pytest.fixture()
def temp_env():
    old_env = os.environ.copy()
    yield
    os.environ = old_env


def add_o3_to_build_system_cflags(pkg, name, flags):
    build_system_flags = []
    if name == 'cflags':
        build_system_flags.append('-O3')
    return (flags, None, build_system_flags)


@pytest.mark.usefixtures('config')
class TestFlagHandlers(object):
    def test_no_build_system_flags(self, temp_env):
        # Test that both autotools and cmake work getting no build_system flags
        s1 = spack.spec.Spec('callpath')
        s1.concretize()
        pkg1 = spack.repo.get(s1)
        spack.build_environment.setup_package(pkg1, False)

        s2 = spack.spec.Spec('libelf')
        s2.concretize()
        pkg2 = spack.repo.get(s2)
        spack.build_environment.setup_package(pkg2, False)

        # Use cppflags as a canary
        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

    def test_unbound_method(self, temp_env):
        # Other tests test flag_handlers set as bound methods and functions.
        # This tests an unbound method in python2 (no change in python3).
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.__class__.inject_flags
        spack.build_environment.setup_package(pkg, False)

        assert os.environ['SPACK_CPPFLAGS'] == '-g'
        assert 'CPPFLAGS' not in os.environ

    def test_inject_flags(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.inject_flags
        spack.build_environment.setup_package(pkg, False)

        assert os.environ['SPACK_CPPFLAGS'] == '-g'
        assert 'CPPFLAGS' not in os.environ

    def test_env_flags(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.env_flags
        spack.build_environment.setup_package(pkg, False)

        assert os.environ['CPPFLAGS'] == '-g'
        assert 'SPACK_CPPFLAGS' not in os.environ

    def test_build_system_flags_cmake(self, temp_env):
        s = spack.spec.Spec('callpath cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

        expected = set(['-DCMAKE_C_FLAGS=-g', '-DCMAKE_CXX_FLAGS=-g',
                        '-DCMAKE_Fortran_FLAGS=-g'])
        assert set(pkg.cmake_flag_args) == expected

    def test_build_system_flags_autotools(self, temp_env):
        s = spack.spec.Spec('libelf cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

        assert 'CPPFLAGS=-g' in pkg.configure_flag_args

    def test_build_system_flags_not_implemented(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.build_system_flags

        # Test the command line flags method raises a NotImplementedError
        try:
            spack.build_environment.setup_package(pkg, False)
            assert False
        except NotImplementedError:
            assert True

    def test_add_build_system_flags_autotools(self, temp_env):
        s = spack.spec.Spec('libelf cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = add_o3_to_build_system_cflags
        spack.build_environment.setup_package(pkg, False)

        assert '-g' in os.environ['SPACK_CPPFLAGS']
        assert 'CPPFLAGS' not in os.environ

        assert pkg.configure_flag_args == ['CFLAGS=-O3']

    def test_add_build_system_flags_cmake(self, temp_env):
        s = spack.spec.Spec('callpath cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = add_o3_to_build_system_cflags
        spack.build_environment.setup_package(pkg, False)

        assert '-g' in os.environ['SPACK_CPPFLAGS']
        assert 'CPPFLAGS' not in os.environ

        assert pkg.cmake_flag_args == ['-DCMAKE_C_FLAGS=-O3']

    def test_ld_flags_cmake(self, temp_env):
        s = spack.spec.Spec('callpath ldflags=-mthreads')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_LDFLAGS' not in os.environ
        assert 'LDFLAGS' not in os.environ

        expected = set(['-DCMAKE_EXE_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_MODULE_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_SHARED_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_STATIC_LINKER_FLAGS=-mthreads'])
        assert set(pkg.cmake_flag_args) == expected

    def test_ld_libs_cmake(self, temp_env):
        s = spack.spec.Spec('callpath ldlibs=-lfoo')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_LDLIBS' not in os.environ
        assert 'LDLIBS' not in os.environ

        expected = set(['-DCMAKE_C_STANDARD_LIBRARIES=-lfoo',
                        '-DCMAKE_CXX_STANDARD_LIBRARIES=-lfoo',
                        '-DCMAKE_Fortran_STANDARD_LIBRARIES=-lfoo'])
        assert set(pkg.cmake_flag_args) == expected
