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

test_branch = 'test-branch'
test_branch_file_name = 'branch-test-file'

test_tag_branch = 'test-tag-branch'
test_tag = 'test-tag'
test_tag_file_name = 'tag-test-file'

untracked = 'foobarbaz'

git = which('git', required=True)

def rev_hash(rev):
    return git('rev-parse', rev, return_output=True).strip()


class GitFetchTest(MockPackagesTest):
    """Tests fetching from a dummy git repository."""

    def setUp(self):
        """Create a git repository with master and two other branches,
           and one tag, so that we can experiment on it."""
        super(GitFetchTest, self).setUp()
        self.stage = Stage('fetch-test')

        self.repo_path = join_path(self.stage.path, test_repo_path)
        mkdirp(self.repo_path)

        self.test_file = join_path(self.repo_path, test_file_name)
        touch(self.test_file)

        with working_dir(self.repo_path):
            git('init')
            git('add', self.test_file)
            git('commit', '-m', 'testing')

            git('branch', test_branch)
            git('branch', test_tag_branch)

            git('checkout', test_branch)
            touch(test_branch_file_name)
            git('add', test_branch_file_name)
            git('commit', '-m' 'branch test')

            git('checkout', test_tag_branch)
            touch(test_tag_file_name)
            git('add', test_tag_file_name)
            git('commit', '-m' 'tag test')
            git('tag', test_tag)

            git('checkout', 'master')

            self.commit = rev_hash(test_tag)

        spec = Spec('git-test')
        spec.concretize()
        self.pkg = spack.db.get(spec, new=True)


    def tearDown(self):
        """Destroy the stage space used by this test."""
        super(GitFetchTest, self).tearDown()

        if self.stage is not None:
            self.stage.destroy()

        self.pkg.do_clean_dist()


    def assert_rev(self, rev):
        """Check that the current git revision is equal to the supplied rev."""
        self.assertEqual(rev_hash('HEAD'), rev_hash(rev))


    def try_fetch(self, rev, test_file, args):
        """Tries to:
           1. Fetch the repo using a fetch strategy constructed with
              supplied args.
           2. Check if the test_file is in the checked out repository.
           3. Assert that the repository is at the revision supplied.
           4. Add and remove some files, then reset the repo, and
              ensure it's all there again.
        """
        self.pkg.versions[ver('git')] = args

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


    def test_fetch_master(self):
        """Test a default git checkout with no commit or tag specified."""
        self.try_fetch('master', test_file_name, {
            'git' : self.repo_path
        })


    def test_fetch_branch(self):
        """Test fetching a branch."""
        self.try_fetch(test_branch, test_branch_file_name, {
            'git'    : self.repo_path,
            'branch' : test_branch
        })


    def test_fetch_tag(self):
        """Test fetching a tag."""
        self.try_fetch(test_tag, test_tag_file_name, {
            'git' : self.repo_path,
            'tag' : test_tag
        })


    def test_fetch_commit(self):
        """Test fetching a particular commit."""
        self.try_fetch(self.commit, test_tag_file_name, {
            'git'    : self.repo_path,
            'commit' : self.commit
        })
