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


class with_tmp(object):
    """Decorator that executes a function with or without spack set to use
       a temp dir.  Spack allows builds to happen directly in the
       stage directory or in a tmp dir and symlinked into the stage
       directory, so this lets us use the same test in both cases.
    """
    def __init__(self, use_tmp):
        self.use_tmp = use_tmp

    def __call__(self, fun):
        use_tmp = self.use_tmp
        def new_test_function(self):
            old_tmp = spack.use_tmp_stage
            spack.use_tmp_stage = use_tmp
            fun(self)
            spack.use_tmp_stage = old_tmp
        return new_test_function


class StageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This sets up a mock archive to fetch, and a mock temp space for use
           by the Stage class.  It doesn't actually create the Stage -- that
           is done by individual tests.
        """
        if os.path.exists(test_files_dir):
            shutil.rmtree(test_files_dir)

        mkdirp(test_files_dir)
        mkdirp(archive_dir_path)
        mkdirp(test_tmp_path)

        with closing(open(test_readme, 'w')) as readme:
            readme.write(readme_text)

        with working_dir(test_files_dir):
            tar = which('tar')
            tar('czf', archive_name, archive_dir)

        # Make spack use the test environment for tmp stuff.
        cls.old_tmp_dirs = spack.tmp_dirs
        spack.tmp_dirs = [test_tmp_path]


    @classmethod
    def tearDownClass(cls):
        """Blows away the test environment directory."""
        shutil.rmtree(test_files_dir)

        # restore spack's original tmp environment
        spack.tmp_dirs = cls.old_tmp_dirs


    def get_stage_path(self, stage, stage_name):
        """Figure out based on a stage and an intended name where it should
           be living.  This depends on whether it's named or not.
        """
        if stage_name:
            # If it is a named stage, we know where the stage should be
            stage_path = join_path(spack.stage_path, stage_name)
        else:
            # If it's unnamed, ensure that we ran mkdtemp in the right spot.
            stage_path = stage.path
            self.assertIsNotNone(stage_path)
            self.assertEqual(
                os.path.commonprefix((stage_path, spack.stage_path)),
                spack.stage_path)
        return stage_path


    def check_setup(self, stage, stage_name):
        """Figure out whether a stage was set up correctly."""
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertTrue(os.path.isdir(stage_path))

        if spack.use_tmp_stage:
            # Make sure everything was created and linked correctly for
            # a tmp stage.
            self.assertTrue(os.path.islink(stage_path))

            target = os.path.realpath(stage_path)
            self.assertTrue(os.path.isdir(target))
            self.assertFalse(os.path.islink(target))
            self.assertEqual(
                os.path.commonprefix((target, test_tmp_path)),
                test_tmp_path)

        else:
            # Make sure the stage path is NOT a link for a non-tmp stage
            self.assertFalse(os.path.islink(stage_path))


    def check_fetch(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertIn(archive_name, os.listdir(stage_path))
        self.assertEqual(join_path(stage_path, archive_name),
                         stage.archive_file)


    def check_expand_archive(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertIn(archive_name, os.listdir(stage_path))
        self.assertIn(archive_dir, os.listdir(stage_path))

        self.assertEqual(
            join_path(stage_path, archive_dir),
            stage.expanded_archive_path)

        readme = join_path(stage_path, archive_dir, readme_name)
        self.assertTrue(os.path.isfile(readme))

        with closing(open(readme)) as file:
            self.assertEqual(readme_text, file.read())


    def check_chdir(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertEqual(os.path.realpath(stage_path), os.getcwd())


    def check_chdir_to_archive(self, stage, stage_name):
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


    def checkSetupAndDestroy(self, stage_name=None):
        stage = Stage(archive_url, name=stage_name)
        self.check_setup(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    @with_tmp(True)
    def test_setup_and_destroy_name_with_tmp(self):
        self.checkSetupAndDestroy(stage_name)


    @with_tmp(False)
    def test_setup_and_destroy_name_without_tmp(self):
        self.checkSetupAndDestroy(stage_name)


    @with_tmp(True)
    def test_setup_and_destroy_no_name_with_tmp(self):
        self.checkSetupAndDestroy(None)


    @with_tmp(False)
    def test_setup_and_destroy_no_name_without_tmp(self):
        self.checkSetupAndDestroy(None)


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
        stage.chdir_to_archive()
        self.check_expand_archive(stage, stage_name)
        self.check_chdir_to_archive(stage, stage_name)

        stage.destroy()
        self.check_destroy(stage, stage_name)


    def test_restage(self):
        stage = Stage(archive_url, name=stage_name)

        stage.fetch()
        stage.expand_archive()
        stage.chdir_to_archive()
        self.check_expand_archive(stage, stage_name)
        self.check_chdir_to_archive(stage, stage_name)

        # Try to make a file in the old archive dir
        with closing(open('foobar', 'w')) as file:
            file.write("this file is to be destroyed.")

        self.assertIn('foobar', os.listdir(stage.expanded_archive_path))

        # Make sure the file is not there after restage.
        stage.restage()
        self.check_chdir(stage, stage_name)
        self.check_fetch(stage, stage_name)

        stage.chdir_to_archive()
        self.check_chdir_to_archive(stage, stage_name)
        self.assertNotIn('foobar', os.listdir(stage.expanded_archive_path))

        stage.destroy()
        self.check_destroy(stage, stage_name)
