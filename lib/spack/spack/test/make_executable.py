##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
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
Tests for Spack's built-in parallel make support.

This just tests whether the right args are getting passed to make.
"""
import os
import unittest
import tempfile
import shutil

from llnl.util.filesystem import *
from spack.util.environment import path_put_first
from spack.build_environment import MakeExecutable


class MakeExecutableTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

        make_exe = join_path(self.tmpdir, 'make')
        with open(make_exe, 'w') as f:
            f.write('#!/bin/sh\n')
            f.write('echo "$@"')
        os.chmod(make_exe, 0700)

        path_put_first('PATH', [self.tmpdir])


    def tearDown(self):
        shutil.rmtree(self.tmpdir)


    def test_make_normal(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(return_output=True).strip(), '-j8')
        self.assertEqual(make('install', return_output=True).strip(), '-j8 install')


    def test_make_explicit(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(parallel=True, return_output=True).strip(), '-j8')
        self.assertEqual(make('install', parallel=True, return_output=True).strip(), '-j8 install')


    def test_make_one_job(self):
        make = MakeExecutable('make', 1)
        self.assertEqual(make(return_output=True).strip(), '')
        self.assertEqual(make('install', return_output=True).strip(), 'install')


    def test_make_parallel_false(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(parallel=False, return_output=True).strip(), '')
        self.assertEqual(make('install', parallel=False, return_output=True).strip(), 'install')


    def test_make_parallel_disabled(self):
        make = MakeExecutable('make', 8)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertEqual(make(return_output=True).strip(), '')
        self.assertEqual(make('install', return_output=True).strip(), 'install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertEqual(make(return_output=True).strip(), '')
        self.assertEqual(make('install', return_output=True).strip(), 'install')

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertEqual(make(return_output=True).strip(), '-j8')
        self.assertEqual(make('install', return_output=True).strip(), '-j8 install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertEqual(make(return_output=True).strip(), '-j8')
        self.assertEqual(make('install', return_output=True).strip(), '-j8 install')

        del os.environ['SPACK_NO_PARALLEL_MAKE']


    def test_make_parallel_precedence(self):
        make = MakeExecutable('make', 8)

        # These should work
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertEqual(make(parallel=True, return_output=True).strip(), '')
        self.assertEqual(make('install', parallel=True, return_output=True).strip(), 'install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertEqual(make(parallel=True, return_output=True).strip(), '')
        self.assertEqual(make('install', parallel=True, return_output=True).strip(), 'install')

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertEqual(make(parallel=True, return_output=True).strip(), '-j8')
        self.assertEqual(make('install', parallel=True, return_output=True).strip(), '-j8 install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertEqual(make(parallel=True, return_output=True).strip(), '-j8')
        self.assertEqual(make('install', parallel=True, return_output=True).strip(), '-j8 install')

        del os.environ['SPACK_NO_PARALLEL_MAKE']
