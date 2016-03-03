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
"""\
Test that the Stage class works correctly.
"""
import unittest
import shutil
import os
import getpass
from contextlib import *

from llnl.util.filesystem import *

import spack
from spack.stage import Stage
from spack.util.executable import which

test_files_dir = join_path(spack.stage_path, '.test')
test_tmp_path  = join_path(test_files_dir, 'tmp')

archive_dir      = 'test-files'
archive_name     = archive_dir + '.tar.gz'
archive_dir_path = join_path(test_files_dir, archive_dir)
archive_url      = 'file://' + join_path(test_files_dir, archive_name)
readme_name      = 'README.txt'
test_readme      = join_path(archive_dir_path, readme_name)
readme_text      = "hello world!\n"

stage_name = 'spack-test-stage'


@contextmanager
def use_tmp(use_tmp):
    """Allow some test code to be executed with spack.use_tmp_stage
       set to a certain value.  Context manager makes sure it's reset
       on failure.
    """
    old_tmp = spack.use_tmp_stage
    spack.use_tmp_stage = use_tmp
    yield
    spack.use_tmp_stage = old_tmp


class StageTest(unittest.TestCase):
    def setUp(self):
        """This sets up a mock archive to fetch, and a mock temp space for use
           by the Stage class.  It doesn't actually create the Stage -- that
           is done by individual tests.
        """
        if os.path.exists(test_files_dir):
            shutil.rmtree(test_files_dir)

        mkdirp(test_files_dir)
        mkdirp(archive_dir_path)
        mkdirp(test_tmp_path)

        with open(test_readme, 'w') as readme:
            readme.write(readme_text)

        with working_dir(test_files_dir):
            tar = which('tar')
            tar('czf', archive_name, archive_dir)

        # Make spack use the test environment for tmp stuff.
        self.old_tmp_dirs = spack.tmp_dirs
        spack.tmp_dirs = [test_tmp_path]

        # record this since this test changes to directories that will
        # be removed.
        self.working_dir = os.getcwd()


    def tearDown(self):
        """Blows away the test environment directory."""
        shutil.rmtree(test_files_dir)

        # chdir back to original working dir
        os.chdir(self.working_dir)

        # restore spack's original tmp environment
        spack.tmp_dirs = self.old_tmp_dirs


    def get_stage_path(self, stage, stage_name):
        """Figure out where a stage should be living.  This depends on
           whether it's named.
        """
        if stage_name is not None:
            # If it is a named stage, we know where the stage should be
            return join_path(spack.stage_path, stage_name)
        else:
            # If it's unnamed, ensure that we ran mkdtemp in the right spot.
            self.assertTrue(stage.path is not None)
            self.assertTrue(stage.path.startswith(spack.stage_path))
            return stage.path


    def check_setup(self, stage, stage_name):
        """Figure out whether a stage was set up correctly."""
        stage_path = self.get_stage_path(stage, stage_name)

        # Ensure stage was created in the spack stage directory
        self.assertTrue(os.path.isdir(stage_path))

        if spack.use_tmp_stage:
            # Check that the stage dir is really a symlink.
            self.assertTrue(os.path.islink(stage_path))

            # Make sure it points to a valid directory
            target = os.path.realpath(stage_path)
            self.assertTrue(os.path.isdir(target))
            self.assertFalse(os.path.islink(target))

            # Make sure the directory is in the place we asked it to
            # be (see setUp and tearDown)
            self.assertTrue(target.startswith(test_tmp_path))

        else:
            # Make sure the stage path is NOT a link for a non-tmp stage
            self.assertFalse(os.path.islink(stage_path))


    def check_fetch(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertTrue(archive_name in os.listdir(stage_path))
        self.assertEqual(join_path(stage_path, archive_name),
                         stage.fetcher.archive_file)


    def check_expand_archive(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertTrue(archive_name in os.listdir(stage_path))
        self.assertTrue(archive_dir in os.listdir(stage_path))

        self.assertEqual(
            join_path(stage_path, archive_dir),
            stage.source_path)

        readme = join_path(stage_path, archive_dir, readme_name)
        self.assertTrue(os.path.isfile(readme))

        with open(readme) as file:
            self.assertEqual(readme_text, file.read())


    def check_chdir(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertEqual(os.path.realpath(stage_path), os.getcwd())


    def check_chdir_to_source(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertEqual(
            join_path(os.path.realpath(stage_path), archive_dir),
            os.getcwd())


    def check_destroy(self, stage, stage_name):
        """Figure out whether a stage was destroyed correctly."""
        stage_path = self.get_stage_path(stage, stage_name)

        # check that the stage dir/link was removed.
        self.assertFalse(os.path.exists(stage_path))

        # tmp stage needs to remove tmp dir too.
        if spack.use_tmp_stage:
            target = os.path.realpath(stage_path)
            self.assertFalse(os.path.exists(target))


    def test_setup_and_destroy_name_with_tmp(self):
        with use_tmp(True):
            stage = Stage(archive_url, name=stage_name)
            self.check_setup(stage, stage_name)

            stage.destroy()
            self.check_destroy(stage, stage_name)


    def test_setup_and_destroy_name_without_tmp(self):
        with use_tmp(False):
            stage = Stage(archive_url, name=stage_name)
            self.check_setup(stage, stage_name)

            stage.destroy()
            self.check_destroy(stage, stage_name)


    def test_setup_and_destroy_no_name_with_tmp(self):
        with use_tmp(True):
            stage = Stage(archive_url)
            self.check_setup(stage, None)

            stage.destroy()
            self.check_destroy(stage, None)


    def test_setup_and_destroy_no_name_without_tmp(self):
        with use_tmp(False):
            stage = Stage(archive_url)
            self.check_setup(stage, None)

            stage.destroy()
            self.check_destroy(stage, None)


    def test_chdir(self):
        stage = Stage(archive_url, name=stage_name)

        stage.chdir()
        self.check_setup(stage, stage_name)
        self.check_chdir(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    def test_fetch(self):
        stage = Stage(archive_url, name=stage_name)

        stage.fetch()
        self.check_setup(stage, stage_name)
        self.check_chdir(stage, stage_name)
        self.check_fetch(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    def test_expand_archive(self):
        stage = Stage(archive_url, name=stage_name)

        stage.fetch()
        self.check_setup(stage, stage_name)
        self.check_fetch(stage, stage_name)

        stage.expand_archive()
        self.check_expand_archive(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    def test_expand_archive(self):
        stage = Stage(archive_url, name=stage_name)

        stage.fetch()
        self.check_setup(stage, stage_name)
        self.check_fetch(stage, stage_name)

        stage.expand_archive()
        stage.chdir_to_source()
        self.check_expand_archive(stage, stage_name)
        self.check_chdir_to_source(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    def test_restage(self):
        stage = Stage(archive_url, name=stage_name)

        stage.fetch()
        stage.expand_archive()
        stage.chdir_to_source()
        self.check_expand_archive(stage, stage_name)
        self.check_chdir_to_source(stage, stage_name)

        # Try to make a file in the old archive dir
        with open('foobar', 'w') as file:
            file.write("this file is to be destroyed.")

        self.assertTrue('foobar' in os.listdir(stage.source_path))

        # Make sure the file is not there after restage.
        stage.restage()
        self.check_chdir(stage, stage_name)
        self.check_fetch(stage, stage_name)

        stage.chdir_to_source()
        self.check_chdir_to_source(stage, stage_name)
        self.assertFalse('foobar' in os.listdir(stage.source_path))

        stage.destroy()
        self.check_destroy(stage, stage_name)
