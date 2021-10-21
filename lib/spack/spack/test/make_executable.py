# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Tests for Spack's built-in parallel make support.

This just tests whether the right args are getting passed to make.
"""
import os
import shutil
import sys
import tempfile
import unittest

import pytest

from spack.build_environment import MakeExecutable
from spack.util.environment import path_put_first


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
class MakeExecutableTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

        make_exe = os.path.join(self.tmpdir, 'make')
        with open(make_exe, 'w') as f:
            f.write('#!/bin/sh\n')
            f.write('echo "$@"')
        os.chmod(make_exe, 0o700)

        path_put_first('PATH', [self.tmpdir])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_make_normal(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(output=str).strip(), '-j8')
        self.assertEqual(make('install', output=str).strip(), '-j8 install')

    def test_make_explicit(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(parallel=True, output=str).strip(), '-j8')
        self.assertEqual(make('install', parallel=True,
                              output=str).strip(), '-j8 install')

    def test_make_one_job(self):
        make = MakeExecutable('make', 1)
        self.assertEqual(make(output=str).strip(), '')
        self.assertEqual(make('install', output=str).strip(), 'install')

    def test_make_parallel_false(self):
        make = MakeExecutable('make', 8)
        self.assertEqual(make(parallel=False, output=str).strip(), '')
        self.assertEqual(make('install', parallel=False,
                              output=str).strip(), 'install')

    def test_make_parallel_disabled(self):
        make = MakeExecutable('make', 8)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertEqual(make(output=str).strip(), '')
        self.assertEqual(make('install', output=str).strip(), 'install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertEqual(make(output=str).strip(), '')
        self.assertEqual(make('install', output=str).strip(), 'install')

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertEqual(make(output=str).strip(), '-j8')
        self.assertEqual(make('install', output=str).strip(), '-j8 install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertEqual(make(output=str).strip(), '-j8')
        self.assertEqual(make('install', output=str).strip(), '-j8 install')

        del os.environ['SPACK_NO_PARALLEL_MAKE']

    def test_make_parallel_precedence(self):
        make = MakeExecutable('make', 8)

        # These should work
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertEqual(make(parallel=True, output=str).strip(), '')
        self.assertEqual(make('install', parallel=True,
                              output=str).strip(), 'install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertEqual(make(parallel=True, output=str).strip(), '')
        self.assertEqual(make('install', parallel=True,
                              output=str).strip(), 'install')

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertEqual(make(parallel=True, output=str).strip(), '-j8')
        self.assertEqual(make('install', parallel=True,
                              output=str).strip(), '-j8 install')

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertEqual(make(parallel=True, output=str).strip(), '-j8')
        self.assertEqual(make('install', parallel=True,
                              output=str).strip(), '-j8 install')

        del os.environ['SPACK_NO_PARALLEL_MAKE']

    def test_make_jobs_env(self):
        make = MakeExecutable('make', 8)
        dump_env = {}
        self.assertEqual(make(output=str, jobs_env='MAKE_PARALLELISM',
                              _dump_env=dump_env).strip(), '-j8')
        self.assertEqual(dump_env['MAKE_PARALLELISM'], '8')
