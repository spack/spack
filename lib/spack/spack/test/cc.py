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
"""
This test checks that the Spack cc compiler wrapper is parsing
arguments correctly.
"""
import os
import unittest

from spack.paths import build_env_path
from spack.util.executable import Executable

# Complicated compiler test command
test_command = [
    '-I/test/include', '-L/test/lib', '-L/other/lib', '-I/other/include',
    'arg1',
    '-Wl,--start-group',
    'arg2',
    '-Wl,-rpath,/first/rpath', 'arg3', '-Wl,-rpath', '-Wl,/second/rpath',
    '-llib1', '-llib2',
    'arg4',
    '-Wl,--end-group',
    '-Xlinker', '-rpath', '-Xlinker', '/third/rpath', '-Xlinker',
    '-rpath', '-Xlinker', '/fourth/rpath',
    '-llib3', '-llib4',
    'arg5', 'arg6']


class CompilerWrapperTest(unittest.TestCase):

    def setUp(self):
        self.cc = Executable(os.path.join(build_env_path, "cc"))
        self.ld = Executable(os.path.join(build_env_path, "ld"))
        self.cpp = Executable(os.path.join(build_env_path, "cpp"))
        self.cxx = Executable(os.path.join(build_env_path, "c++"))
        self.fc = Executable(os.path.join(build_env_path, "fc"))

        self.realcc = "/bin/mycc"
        self.prefix = "/spack-test-prefix"

        os.environ['SPACK_CC'] = self.realcc
        os.environ['SPACK_CXX'] = self.realcc
        os.environ['SPACK_FC'] = self.realcc

        os.environ['SPACK_PREFIX'] = self.prefix
        os.environ['SPACK_ENV_PATH'] = "test"
        os.environ['SPACK_DEBUG_LOG_DIR'] = "."
        os.environ['SPACK_DEBUG_LOG_ID'] = "foo-hashabc"
        os.environ['SPACK_COMPILER_SPEC'] = "gcc@4.4.7"
        os.environ['SPACK_SHORT_SPEC'] = (
            "foo@1.2 arch=linux-rhel6-x86_64 /hashabc")

        os.environ['SPACK_CC_RPATH_ARG']  = "-Wl,-rpath,"
        os.environ['SPACK_CXX_RPATH_ARG'] = "-Wl,-rpath,"
        os.environ['SPACK_F77_RPATH_ARG'] = "-Wl,-rpath,"
        os.environ['SPACK_FC_RPATH_ARG']  = "-Wl,-rpath,"

        self.path1 = '/x/y/z1/'
        self.path2 = '/x/y/z2/'
        self.path3 = '/x/y/z3/'

        if 'SPACK_LINK_DIRS' in os.environ:
            del os.environ['SPACK_LINK_DIRS']

        if 'SPACK_RPATH_DIRS' in os.environ:
            del os.environ['SPACK_RPATH_DIRS']

        if 'SPACK_INCLUDE_DIRS' in os.environ:
            del os.environ['SPACK_INCLUDE_DIRS']

    def check_cc(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.cc(*args, output=str).strip(), expected)

    def check_cxx(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.cxx(*args, output=str).strip(), expected)

    def check_fc(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.fc(*args, output=str).strip(), expected)

    def check_ld(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.ld(*args, output=str).strip(), expected)

    def check_cpp(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.cpp(*args, output=str).strip(), expected)

    def test_vcheck_mode(self):
        self.check_cc('dump-mode', ['-I/include', '--version'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-V'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-v'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-dumpversion'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '--version', '-c'], "vcheck")
        self.check_cc('dump-mode', ['-I/include',
                                    '-V', '-o', 'output'], "vcheck")

    def test_cpp_mode(self):
        self.check_cc('dump-mode', ['-E'], "cpp")
        self.check_cpp('dump-mode', [], "cpp")

    def test_as_mode(self):
        self.check_cc('dump-mode', ['-S'], "as")

    def test_ccld_mode(self):
        self.check_cc('dump-mode', [], "ccld")
        self.check_cc('dump-mode', ['foo.c', '-o', 'foo'], "ccld")
        self.check_cc('dump-mode', ['foo.c', '-o',
                                    'foo', '-Wl,-rpath,foo'], "ccld")
        self.check_cc(
            'dump-mode',
            ['foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo'],
            "ccld")

    def test_ld_mode(self):
        self.check_ld('dump-mode', [], "ld")
        self.check_ld(
            'dump-mode',
            ['foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo'],
            "ld")

    def test_flags(self):
        os.environ['SPACK_LDFLAGS'] = '-L foo'
        os.environ['SPACK_LDLIBS'] = '-lfoo'
        os.environ['SPACK_CPPFLAGS'] = '-g -O1'
        os.environ['SPACK_CFLAGS'] = '-Wall'
        os.environ['SPACK_CXXFLAGS'] = '-Werror'
        os.environ['SPACK_FFLAGS'] = '-w'

        try:
            # Test ldflags added properly in ld mode
            self.check_ld('dump-args', test_command,
                          "ld " +
                          '-L foo ' +
                          ' '.join(test_command) + ' ' +
                          '-lfoo')

            # Test cppflags added properly in cpp mode
            self.check_cpp('dump-args', test_command,
                           "cpp " +
                           '-g -O1 ' +
                           ' '.join(test_command))

            # Test ldflags, cppflags, and language specific flags are added in
            # proper order
            self.check_cc('dump-args', test_command,
                          self.realcc + ' ' +
                          '-g -O1 ' +
                          '-Wall ' +
                          '-L foo ' +
                          ' '.join(test_command) + ' ' +
                          '-lfoo')

            self.check_cxx('dump-args', test_command,
                           self.realcc + ' ' +
                           '-g -O1 ' +
                           '-Werror ' +
                           '-L foo ' +
                           ' '.join(test_command) + ' ' +
                           '-lfoo')

            self.check_fc('dump-args', test_command,
                          self.realcc + ' ' +
                          '-w ' +
                          '-g -O1 ' +
                          '-L foo ' +
                          ' '.join(test_command) + ' ' +
                          '-lfoo')
        finally:
            del os.environ['SPACK_CFLAGS']
            del os.environ['SPACK_CXXFLAGS']
            del os.environ['SPACK_FFLAGS']
            del os.environ['SPACK_CPPFLAGS']
            del os.environ['SPACK_LDFLAGS']
            del os.environ['SPACK_LDLIBS']

    def test_dep_include(self):
        """Ensure a single dependency include directory is added."""
        os.environ['SPACK_INCLUDE_DIRS'] = ':'.join([self.path3])
        self.check_cc('dump-args', test_command,
                      self.realcc + ' ' +
                      '-I' + self.path3 + ' ' +
                      ' '.join(test_command))

    def test_dep_lib_no_rpath(self):
        """Ensure a single dependency link flag is added with no dep RPATH."""
        os.environ['SPACK_LINK_DIRS'] = ':'.join([self.path1])
        self.check_cc('dump-args', test_command,
                      self.realcc + ' ' +
                      '-L' + self.path1 + ' ' +
                      ' '.join(test_command))

    def test_dep_lib_no_lib(self):
        """Ensure a single dependency RPATH is added with no -L."""
        os.environ['SPACK_RPATH_DIRS'] = ':'.join([self.path1])
        self.check_cc('dump-args', test_command,
                      self.realcc + ' ' +
                      '-Wl,-rpath,' + self.path1 + ' ' +
                      ' '.join(test_command))

    def test_all_deps(self):
        """Ensure includes and RPATHs for all deps are added. """
        os.environ['SPACK_LINK_DIRS'] = ':'.join([self.path1, self.path2])
        os.environ['SPACK_RPATH_DIRS'] = ':'.join([self.path2])
        os.environ['SPACK_INCLUDE_DIRS'] = ':'.join([self.path3])

        # This is probably more constrained than it needs to be; it
        # checks order within prepended args and doesn't strictly have
        # to.  We could loosen that if it becomes necessary
        self.check_cc('dump-args', test_command,
                      self.realcc + ' ' +
                      '-L' + self.path2 + ' ' +
                      '-L' + self.path1 + ' ' +

                      '-Wl,-rpath,' + self.path2 + ' ' +

                      '-I' + self.path3 + ' ' +

                      ' '.join(test_command))

    def test_ld_deps(self):
        """Ensure no (extra) -I args or -Wl, are passed in ld mode."""
        os.environ['SPACK_LINK_DIRS'] = ':'.join([self.path1, self.path2])
        os.environ['SPACK_RPATH_DIRS'] = ':'.join([self.path2])

        self.check_ld('dump-args', test_command,
                      'ld ' +
                      '-L' + self.path2 + ' ' +
                      '-L' + self.path1 + ' ' +

                      '-rpath ' + self.path2 + ' ' +

                      ' '.join(test_command))

    def test_ld_deps_no_link(self):
        """Ensure SPACK_LINK_DEPS controls -L for ld."""
        os.environ['SPACK_RPATH_DIRS'] = ':'.join([self.path1, self.path2])

        self.check_ld('dump-args', test_command,
                      'ld ' +
                      '-rpath ' + self.path2 + ' ' +
                      '-rpath ' + self.path1 + ' ' +

                      ' '.join(test_command))

    def test_ld_deps_reentrant(self):
        """Make sure ld -r is handled correctly on OS's where it doesn't
           support rpaths."""
        os.environ['SPACK_LINK_DIRS'] = ':'.join([self.path1])
        os.environ['SPACK_RPATH_DIRS'] = ':'.join([self.path1])

        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=linux-x86_64"
        reentrant_test_command = ['-r'] + test_command
        self.check_ld('dump-args', reentrant_test_command,
                      'ld ' +

                      '-L' + self.path1 + ' ' +
                      '-rpath ' + self.path1 + ' '

                      '-r ' +
                      ' '.join(test_command))

        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=darwin-x86_64"
        self.check_ld('dump-args', reentrant_test_command,
                      'ld ' +
                      '-L' + self.path1 + ' ' +
                      '-r ' +
                      ' '.join(test_command))
