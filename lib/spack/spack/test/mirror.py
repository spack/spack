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
import os
from filecmp import dircmp

import spack
import spack.mirror
from spack.util.compression import decompressor_for
from spack.test.mock_packages_test import *
from spack.test.mock_repo import *

# paths in repos that shouldn't be in the mirror tarballs.
exclude = ['.hg', '.git', '.svn']


class MirrorTest(MockPackagesTest):
    def setUp(self):
        """Sets up a mock package and a mock repo for each fetch strategy, to
           ensure that the mirror can create archives for each of them.
        """
        super(MirrorTest, self).setUp()
        self.repos = {}


    def set_up_package(self, name, MockRepoClass, url_attr):
        """Use this to set up a mock package to be mirrored.
           Each package needs us to:
             1. Set up a mock repo/archive to fetch from.
             2. Point the package's version args at that repo.
        """
        # Set up packages to point at mock repos.
        spec = Spec(name)
        spec.concretize()

        # Get the package and fix its fetch args to point to a mock repo
        pkg = spack.db.get(spec)
        repo = MockRepoClass()
        self.repos[name] = repo

        # change the fetch args of the first (only) version.
        assert(len(pkg.versions) == 1)
        v = next(iter(pkg.versions))
        pkg.versions[v][url_attr] = repo.url


    def tearDown(self):
        """Destroy all the stages created by the repos in setup."""
        super(MirrorTest, self).tearDown()

        for name, repo in self.repos.items():
            if repo.stage:
                pass #repo.stage.destroy()

        self.repos.clear()


    def check_mirror(self):
        stage = Stage('spack-mirror-test')
        mirror_root = join_path(stage.path, 'test-mirror')

        try:
            os.chdir(stage.path)
            spack.mirror.create(
                mirror_root, self.repos, no_checksum=True)

            # Stage directory exists
            self.assertTrue(os.path.isdir(mirror_root))

            # subdirs for each package
            for name in self.repos:
                subdir = join_path(mirror_root, name)
                self.assertTrue(os.path.isdir(subdir))

                files = os.listdir(subdir)
                self.assertEqual(len(files), 1)

                # Decompress archive in the mirror
                archive = files[0]
                archive_path = join_path(subdir, archive)
                decomp = decompressor_for(archive_path)

                with working_dir(subdir):
                    decomp(archive_path)

                    # Find the untarred archive directory.
                    files = os.listdir(subdir)
                    self.assertEqual(len(files), 2)
                    self.assertTrue(archive in files)
                    files.remove(archive)

                    expanded_archive = join_path(subdir, files[0])
                    self.assertTrue(os.path.isdir(expanded_archive))

                    # Compare the original repo with the expanded archive
                    repo = self.repos[name]
                    if not 'svn' in name:
                        original_path = repo.path
                    else:
                        co = 'checked_out'
                        svn('checkout', repo.url, co)
                        original_path = join_path(subdir, co)

                    dcmp = dircmp(original_path, expanded_archive)

                    # make sure there are no new files in the expanded tarball
                    self.assertFalse(dcmp.right_only)
                    self.assertTrue(all(l in exclude for l in dcmp.left_only))

        finally:
            pass #stage.destroy()


    def test_git_mirror(self):
        self.set_up_package('git-test', MockGitRepo, 'git')
        self.check_mirror()

    def test_svn_mirror(self):
        self.set_up_package('svn-test', MockSvnRepo, 'svn')
        self.check_mirror()

    def test_hg_mirror(self):
        self.set_up_package('hg-test', MockHgRepo, 'hg')
        self.check_mirror()

    def test_url_mirror(self):
        self.set_up_package('trivial_install_test_package', MockArchive, 'url')
        self.check_mirror()

    def test_all_mirror(self):
        self.set_up_package('git-test', MockGitRepo, 'git')
        self.set_up_package('svn-test', MockSvnRepo, 'svn')
        self.set_up_package('hg-test',  MockHgRepo,  'hg')
        self.set_up_package('trivial_install_test_package', MockArchive, 'url')
        self.check_mirror()
