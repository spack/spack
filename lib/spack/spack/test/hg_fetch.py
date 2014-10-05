##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import os
import unittest
import shutil
import tempfile
from contextlib import closing

from llnl.util.filesystem import *

import spack
from spack.version import ver
from spack.stage import Stage
from spack.util.executable import which
from spack.test.mock_packages_test import *

test_repo_path = 'test-repo'
test_file_name = 'test-file.txt'
test_rev1_file_name = 'test-file2.txt'
untracked = 'foobarbaz'

hg = which('hg', required=True)

class HgFetchTest(MockPackagesTest):
    """Tests fetching from a dummy hg repository."""

    def get_rev(self):
        """Get current mercurial revision."""
        return hg('id', '-i', return_output=True).strip()


    def setUp(self):
        """Create a hg repository with master and two other branches,
           and one tag, so that we can experiment on it."""
        super(HgFetchTest, self).setUp()
        self.stage = Stage('fetch-test')

        self.repo_path = join_path(self.stage.path, test_repo_path)
        mkdirp(self.repo_path)

        test_file      = join_path(self.repo_path, test_file_name)
        test_file_rev1 = join_path(self.repo_path, test_rev1_file_name)

        with working_dir(self.repo_path):
            hg('init')

            touch(test_file)
            hg('add', test_file)
            hg('commit', '-m', 'revision 0', '-u', 'test')
            self.rev0 = self.get_rev()

            touch(test_file_rev1)
            hg('add', test_file_rev1)
            hg('commit', '-m' 'revision 1', '-u', 'test')
            self.rev1 = self.get_rev()

        spec = Spec('hg-test')
        spec.concretize()
        self.pkg = spack.db.get(spec, new=True)


    def tearDown(self):
        """Destroy the stage space used by this test."""
        super(HgFetchTest, self).tearDown()

        if self.stage is not None:
            self.stage.destroy()

        self.pkg.do_clean_dist()


    def assert_rev(self, rev):
        """Check that the current hg revision is equal to the supplied rev."""
        self.assertEqual(self.get_rev(), rev)


    def try_fetch(self, rev, test_file, args):
        """Tries to:
           1. Fetch the repo using a fetch strategy constructed with
              supplied args.
           2. Check if the test_file is in the checked out repository.
           3. Assert that the repository is at the revision supplied.
           4. Add and remove some files, then reset the repo, and
              ensure it's all there again.
        """
        self.pkg.versions[ver('hg')] = args

        self.pkg.do_stage()
        self.assert_rev(rev)

        file_path = join_path(self.pkg.stage.source_path, test_file)
        self.assertTrue(os.path.isdir(self.pkg.stage.source_path))
        self.assertTrue(os.path.isfile(file_path))

        os.unlink(file_path)
        self.assertFalse(os.path.isfile(file_path))

        touch(untracked)
        self.assertTrue(os.path.isfile(untracked))
        self.pkg.do_clean_work()
        self.assertFalse(os.path.isfile(untracked))

        self.assertTrue(os.path.isdir(self.pkg.stage.source_path))
        self.assertTrue(os.path.isfile(file_path))

        self.assert_rev(rev)


    def test_fetch_default(self):
        """Test a default hg checkout with no commit or tag specified."""
        self.try_fetch(self.rev1, test_rev1_file_name, {
            'hg' : self.repo_path
        })


    def test_fetch_rev0(self):
        """Test fetching a branch."""
        self.try_fetch(self.rev0, test_file_name, {
            'hg'       : self.repo_path,
            'revision' : self.rev0
        })
