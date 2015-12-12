##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
This test checks that the Spack cc compiler wrapper is parsing
arguments correctly.
"""
import os
import unittest

from llnl.util.filesystem import *
import spack
from spack.util.executable import *

# Complicated compiler test command
test_command = [
    '-I/test/include', '-L/test/lib', '-L/other/lib', '-I/other/include',
    'arg1',
    '-Wl,--start-group',
    'arg2',
    '-Wl,-rpath=/first/rpath', 'arg3', '-Wl,-rpath', '-Wl,/second/rpath',
    '-llib1', '-llib2',
    'arg4',
    '-Wl,--end-group',
    '-Xlinker,-rpath', '-Xlinker,/third/rpath', '-Xlinker,-rpath=/fourth/rpath',
    '-llib3', '-llib4',
    'arg5', 'arg6']


class CompilerTest(unittest.TestCase):

    def setUp(self):
        self.cc = Executable(join_path(spack.build_env_path, "cc"))
        self.ld = Executable(join_path(spack.build_env_path, "ld"))
        self.cpp = Executable(join_path(spack.build_env_path, "cpp"))

        os.environ['SPACK_CC'] = "/bin/mycc"
        os.environ['SPACK_PREFIX'] = "/usr"
        os.environ['SPACK_ENV_PATH']="test"
        os.environ['SPACK_DEBUG_LOG_DIR'] = "."
        os.environ['SPACK_COMPILER_SPEC'] = "gcc@4.4.7"
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2"


    def check_cc(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.cc(*args, return_output=True).strip(), expected)


    def check_ld(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.ld(*args, return_output=True).strip(), expected)


    def check_cpp(self, command, args, expected):
        os.environ['SPACK_TEST_COMMAND'] = command
        self.assertEqual(self.cpp(*args, return_output=True).strip(), expected)


    def test_vcheck_mode(self):
        self.check_cc('dump-mode', ['-I/include', '--version'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-V'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-v'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-dumpversion'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '--version', '-c'], "vcheck")
        self.check_cc('dump-mode', ['-I/include', '-V', '-o', 'output'], "vcheck")


    def test_cpp_mode(self):
        self.check_cc('dump-mode', ['-E'], "cpp")
        self.check_cpp('dump-mode', [], "cpp")


    def test_ccld_mode(self):
        self.check_cc('dump-mode', [], "ccld")
        self.check_cc('dump-mode', ['foo.c', '-o', 'foo'], "ccld")
        self.check_cc('dump-mode', ['foo.c', '-o', 'foo', '-Wl,-rpath=foo'], "ccld")
        self.check_cc('dump-mode', ['foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath=foo'], "ccld")


    def test_ld_mode(self):
        self.check_ld('dump-mode', [], "ld")
        self.check_ld('dump-mode', ['foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath=foo'], "ld")


    def test_includes(self):
        self.check_cc('dump-includes', test_command,
                      "\n".join(["/test/include", "/other/include"]))


    def test_libraries(self):
        self.check_cc('dump-libraries', test_command,
                      "\n".join(["/test/lib", "/other/lib"]))


    def test_libs(self):
        self.check_cc('dump-libs', test_command,
                      "\n".join(["lib1", "lib2", "lib3", "lib4"]))


    def test_rpaths(self):
        self.check_cc('dump-rpaths', test_command,
                      "\n".join(["/first/rpath", "/second/rpath", "/third/rpath", "/fourth/rpath"]))


    def test_other_args(self):
        self.check_cc('dump-other-args', test_command,
                      "\n".join(["arg1", "-Wl,--start-group", "arg2", "arg3", "arg4",
                                 "-Wl,--end-group", "arg5", "arg6"]))
