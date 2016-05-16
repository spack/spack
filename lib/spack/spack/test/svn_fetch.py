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
import os
import re
import spack

from spack.test.mock_repo import svn, MockSvnRepo
from spack.version import ver
from spack.test.mock_packages_test import *
from llnl.util.filesystem import *


class SvnFetchTest(MockPackagesTest):
    """Tests fetching from a dummy git repository."""

    def setUp(self):
        """Create an svn repository with two revisions."""
        super(SvnFetchTest, self).setUp()

        self.repo = MockSvnRepo()

        spec = Spec('svn-test')
        spec.concretize()
        self.pkg = spack.repo.get(spec, new=True)

    def tearDown(self):
        """Destroy the stage space used by this test."""
        super(SvnFetchTest, self).tearDown()
        self.repo.destroy()

    def assert_rev(self, rev):
        """Check that the current revision is equal to the supplied rev."""
        def get_rev():
            output = svn('info', output=str)
            self.assertTrue("Revision" in output)
            for line in output.split('\n'):
                match = re.match(r'Revision: (\d+)', line)
                if match:
                    return match.group(1)
        self.assertEqual(get_rev(), rev)

    def try_fetch(self, rev, test_file, args):
        """Tries to:
           1. Fetch the repo using a fetch strategy constructed with
              supplied args.
           2. Check if the test_file is in the checked out repository.
           3. Assert that the repository is at the revision supplied.
           4. Add and remove some files, then reset the repo, and
              ensure it's all there again.
        """
        self.pkg.versions[ver('svn')] = args

        with self.pkg.stage:
            self.pkg.do_stage()
            self.assert_rev(rev)

            file_path = join_path(self.pkg.stage.source_path, test_file)
            self.assertTrue(os.path.isdir(self.pkg.stage.source_path))
            self.assertTrue(os.path.isfile(file_path))

            os.unlink(file_path)
            self.assertFalse(os.path.isfile(file_path))

            untracked = 'foobarbaz'
            touch(untracked)
            self.assertTrue(os.path.isfile(untracked))
            self.pkg.do_restage()
            self.assertFalse(os.path.isfile(untracked))

            self.assertTrue(os.path.isdir(self.pkg.stage.source_path))
            self.assertTrue(os.path.isfile(file_path))

            self.assert_rev(rev)


    def test_fetch_default(self):
        """Test a default checkout and make sure it's on rev 1"""
        self.try_fetch(self.repo.r1, self.repo.r1_file, {
            'svn' : self.repo.url
        })


    def test_fetch_r1(self):
        """Test fetching an older revision (0)."""
        self.try_fetch(self.repo.r0, self.repo.r0_file, {
            'svn'      : self.repo.url,
            'revision' : self.repo.r0
        })
