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

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="MakeExecutable \
                                        not supported on Windows",
)


class MakeExecutableTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

        make_exe = os.path.join(self.tmpdir, "make")
        with open(make_exe, "w") as f:
            f.write("#!/bin/sh\n")
            f.write('echo "$@"')
        os.chmod(make_exe, 0o700)

        path_put_first("PATH", [self.tmpdir])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    if sys.version_info < (3, 1):
        def assertIn(self, a, b):
            self.assertTrue(a in b)

    def test_make_normal(self):
        make = MakeExecutable('make', 8)
        self.assertIn('-j8', make(output=str).strip().split())
        inst = make('install', output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

    def test_make_explicit(self):
        make = MakeExecutable('make', 8)
        self.assertIn('-j8', make(parallel=True, output=str).strip().split())
        inst = make('install', parallel=True, output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

    def test_make_one_job(self):
        make = MakeExecutable('make', 1)
        self.assertFalse('-j' in make(output=str).strip())
        inst = make('install', output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

    def test_make_parallel_false(self):
        make = MakeExecutable('make', 8)
        self.assertFalse('-j' in make(output=str, parallel=False).strip())
        inst = make('install', parallel=False, output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

    def test_make_parallel_disabled(self):
        make = MakeExecutable("make", 8)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertFalse('-j' in make(output=str).strip())
        inst = make('install', output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertFalse('-j' in make(output=str).strip())
        inst = make('install', output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertIn('-j8', make(output=str).strip().split())
        inst = make('install', output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertIn('-j8', make(output=str).strip().split())
        inst = make('install', output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

        del os.environ["SPACK_NO_PARALLEL_MAKE"]

    def test_make_parallel_precedence(self):
        make = MakeExecutable("make", 8)

        # These should work
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'true'
        self.assertFalse('-j' in make(output=str, parallel=True).strip())
        inst = make('install', parallel=True, output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = '1'
        self.assertFalse('-j' in make(output=str, parallel=True).strip())
        inst = make('install', parallel=True, output=str).strip()
        self.assertIn('install', inst)
        self.assertFalse('-j' in inst)

        # These don't disable (false and random string)
        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'false'
        self.assertIn('-j8', make(parallel=True, output=str).strip().split())
        inst = make('install', parallel=True, output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

        os.environ['SPACK_NO_PARALLEL_MAKE'] = 'foobar'
        self.assertIn('-j8', make(parallel=True, output=str).strip().split())
        inst = make('install', parallel=True, output=str).strip().split()
        self.assertIn('-j8', inst)
        self.assertIn('install', inst)

        del os.environ["SPACK_NO_PARALLEL_MAKE"]

    def test_make_jobs_env(self):
        make = MakeExecutable("make", 8)
        dump_env = {}
        self.assertIn('-j8', make(output=str, jobs_env='MAKE_PARALLELISM',
                                  _dump_env=dump_env).strip().split())
        self.assertEqual(dump_env['MAKE_PARALLELISM'], '8')
