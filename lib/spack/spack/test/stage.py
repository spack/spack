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
"""\
Test that the Stage class works correctly.
"""
import os
import shutil
import tempfile
from contextlib import *

import spack
import spack.stage
from llnl.util.filesystem import *
from spack.stage import Stage
from spack.util.executable import which
from spack.test.mock_packages_test import *

_test_tmp_path = None


@contextmanager
def use_tmp(use_tmp):
    """Allow some test code to be executed such that spack will either use or
       not use temporary space for stages.
    """
    # mock up config
    assert(_test_tmp_path is not None)

    if use_tmp:
        path = _test_tmp_path    # use temporary stage
    else:
        path = spack.stage_path  # Use Spack's stage dir (no links)

    spack.config.update_config(
        'config', {'build_stage': [path]}, scope='user')

    yield


def fail_search_fn():
    raise Exception("This should not have been called")


class FailingFetchStrategy(spack.fetch_strategy.FetchStrategy):
    def fetch(self):
        raise spack.fetch_strategy.FailedDownloadError(
            "<non-existent URL>",
            "This implementation of FetchStrategy always fails")


class MockSearchFunction(object):
    def __init__(self):
        self.performed_search = False

    def __call__(self):
        self.performed_search = True
        return []


class StageTest(MockPackagesTest):

    def setUp(self):
        """This sets up a mock archive to fetch, and a mock temp space for use
           by the Stage class.  It doesn't actually create the Stage -- that
           is done by individual tests.
        """
        super(StageTest, self).setUp()

        global _test_tmp_path

        #
        # Mock up a stage area that looks like this:
        #
        # TMPDIR/                    test_files_dir
        #     tmp/                   test_tmp_path (where stage should be)
        #     test-files/            archive_dir_path
        #         README.txt         test_readme (contains "hello world!\n")
        #     test-files.tar.gz      archive_url = file:///path/to/this
        #
        self.test_files_dir = tempfile.mkdtemp()
        self.test_tmp_path  = os.path.realpath(
            os.path.join(self.test_files_dir, 'tmp'))
        _test_tmp_path = self.test_tmp_path

        # set _test_tmp_path as the default test directory to use for stages.
        spack.config.update_config(
            'config', {'build_stage': [_test_tmp_path]}, scope='user')

        self.archive_dir = 'test-files'
        self.archive_name = self.archive_dir + '.tar.gz'
        archive_dir_path = os.path.join(self.test_files_dir,
                                        self.archive_dir)
        self.archive_url = 'file://' + os.path.join(self.test_files_dir,
                                                    self.archive_name)
        test_readme = join_path(archive_dir_path, 'README.txt')
        self.readme_text = "hello world!\n"

        self.stage_name = 'spack-test-stage'

        mkdirp(archive_dir_path)
        mkdirp(self.test_tmp_path)

        with open(test_readme, 'w') as readme:
            readme.write(self.readme_text)

        with working_dir(self.test_files_dir):
            tar = which('tar', required=True)
            tar('czf', self.archive_name, self.archive_dir)

        # Make spack use the test environment for tmp stuff.
        self._old_tmp_root = spack.stage._tmp_root
        self._old_use_tmp_stage = spack.stage._use_tmp_stage
        spack.stage._tmp_root = None
        spack.stage._use_tmp_stage = True

        # record this since this test changes to directories that will
        # be removed.
        self.working_dir = os.getcwd()

    def tearDown(self):
        """Blows away the test environment directory."""
        super(StageTest, self).tearDown()

        shutil.rmtree(self.test_files_dir, ignore_errors=True)

        # chdir back to original working dir
        os.chdir(self.working_dir)

        # restore spack's original tmp environment
        spack.stage._tmp_root = self._old_tmp_root
        spack.stage._use_tmp_stage = self._old_use_tmp_stage

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

        if spack.stage.get_tmp_root():
            # Check that the stage dir is really a symlink.
            self.assertTrue(os.path.islink(stage_path))

            # Make sure it points to a valid directory
            target = os.path.realpath(stage_path)
            self.assertTrue(os.path.isdir(target))
            self.assertFalse(os.path.islink(target))

            # Make sure the directory is in the place we asked it to
            # be (see setUp, tearDown, and use_tmp)
            self.assertTrue(target.startswith(self.test_tmp_path))

        else:
            # Make sure the stage path is NOT a link for a non-tmp stage
            self.assertFalse(os.path.islink(stage_path))

    def check_fetch(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertTrue(self.archive_name in os.listdir(stage_path))
        self.assertEqual(join_path(stage_path, self.archive_name),
                         stage.fetcher.archive_file)

    def check_expand_archive(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertTrue(self.archive_name in os.listdir(stage_path))
        self.assertTrue(self.archive_dir in os.listdir(stage_path))

        self.assertEqual(
            join_path(stage_path, self.archive_dir),
            stage.source_path)

        readme = join_path(stage_path, self.archive_dir, 'README.txt')
        self.assertTrue(os.path.isfile(readme))

        with open(readme) as file:
            self.assertEqual(self.readme_text, file.read())

    def check_chdir(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertEqual(os.path.realpath(stage_path), os.getcwd())

    def check_chdir_to_source(self, stage, stage_name):
        stage_path = self.get_stage_path(stage, stage_name)
        self.assertEqual(
            join_path(os.path.realpath(stage_path), self.archive_dir),
            os.getcwd())

    def check_destroy(self, stage, stage_name):
        """Figure out whether a stage was destroyed correctly."""
        stage_path = self.get_stage_path(stage, stage_name)

        # check that the stage dir/link was removed.
        self.assertFalse(os.path.exists(stage_path))

        # tmp stage needs to remove tmp dir too.
        if spack.stage._use_tmp_stage:
            target = os.path.realpath(stage_path)
            self.assertFalse(os.path.exists(target))

    def test_setup_and_destroy_name_with_tmp(self):
        with use_tmp(True):
            with Stage(self.archive_url, name=self.stage_name) as stage:
                self.check_setup(stage, self.stage_name)
            self.check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_name_without_tmp(self):
        with use_tmp(False):
            with Stage(self.archive_url, name=self.stage_name) as stage:
                self.check_setup(stage, self.stage_name)
            self.check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_no_name_with_tmp(self):
        with use_tmp(True):
            with Stage(self.archive_url) as stage:
                self.check_setup(stage, None)
            self.check_destroy(stage, None)

    def test_setup_and_destroy_no_name_without_tmp(self):
        with use_tmp(False):
            with Stage(self.archive_url) as stage:
                self.check_setup(stage, None)
            self.check_destroy(stage, None)

    def test_chdir(self):
        with Stage(self.archive_url, name=self.stage_name) as stage:
            stage.chdir()
            self.check_setup(stage, self.stage_name)
            self.check_chdir(stage, self.stage_name)
        self.check_destroy(stage, self.stage_name)

    def test_fetch(self):
        with Stage(self.archive_url, name=self.stage_name) as stage:
            stage.fetch()
            self.check_setup(stage, self.stage_name)
            self.check_chdir(stage, self.stage_name)
            self.check_fetch(stage, self.stage_name)
        self.check_destroy(stage, self.stage_name)

    def test_no_search_if_default_succeeds(self):
        with Stage(self.archive_url, name=self.stage_name,
                   search_fn=fail_search_fn) as stage:
            stage.fetch()
        self.check_destroy(stage, self.stage_name)

    def test_no_search_mirror_only(self):
        with Stage(FailingFetchStrategy(), name=self.stage_name,
                   search_fn=fail_search_fn) as stage:
            try:
                stage.fetch(mirror_only=True)
            except spack.fetch_strategy.FetchError:
                pass
        self.check_destroy(stage, self.stage_name)

    def test_search_if_default_fails(self):
        test_search = MockSearchFunction()
        with Stage(FailingFetchStrategy(), name=self.stage_name,
                   search_fn=test_search) as stage:
            try:
                stage.fetch(mirror_only=False)
            except spack.fetch_strategy.FetchError:
                pass
        self.check_destroy(stage, self.stage_name)
        self.assertTrue(test_search.performed_search)

    def test_expand_archive(self):
        with Stage(self.archive_url, name=self.stage_name) as stage:
            stage.fetch()
            self.check_setup(stage, self.stage_name)
            self.check_fetch(stage, self.stage_name)
            stage.expand_archive()
            self.check_expand_archive(stage, self.stage_name)
        self.check_destroy(stage, self.stage_name)

    def test_expand_archive_with_chdir(self):
        with Stage(self.archive_url, name=self.stage_name) as stage:
            stage.fetch()
            self.check_setup(stage, self.stage_name)
            self.check_fetch(stage, self.stage_name)
            stage.expand_archive()
            stage.chdir_to_source()
            self.check_expand_archive(stage, self.stage_name)
            self.check_chdir_to_source(stage, self.stage_name)
        self.check_destroy(stage, self.stage_name)

    def test_restage(self):
        with Stage(self.archive_url, name=self.stage_name) as stage:
            stage.fetch()
            stage.expand_archive()
            stage.chdir_to_source()
            self.check_expand_archive(stage, self.stage_name)
            self.check_chdir_to_source(stage, self.stage_name)

            # Try to make a file in the old archive dir
            with open('foobar', 'w') as file:
                file.write("this file is to be destroyed.")

            self.assertTrue('foobar' in os.listdir(stage.source_path))

            # Make sure the file is not there after restage.
            stage.restage()
            self.check_chdir(stage, self.stage_name)
            self.check_fetch(stage, self.stage_name)
            stage.chdir_to_source()
            self.check_chdir_to_source(stage, self.stage_name)
            self.assertFalse('foobar' in os.listdir(stage.source_path))
        self.check_destroy(stage, self.stage_name)

    def test_no_keep_without_exceptions(self):
        with Stage(self.archive_url,
                   name=self.stage_name, keep=False) as stage:
            pass
        self.check_destroy(stage, self.stage_name)

    def test_keep_without_exceptions(self):
        with Stage(self.archive_url,
                   name=self.stage_name, keep=True) as stage:
            pass
        path = self.get_stage_path(stage, self.stage_name)
        self.assertTrue(os.path.isdir(path))

    def test_no_keep_with_exceptions(self):
        try:
            with Stage(self.archive_url,
                       name=self.stage_name, keep=False) as stage:
                raise Exception()

            path = self.get_stage_path(stage, self.stage_name)
            self.assertTrue(os.path.isdir(path))
        except:
            pass  # ignore here.

    def test_keep_exceptions(self):
        try:
            with Stage(self.archive_url,
                       name=self.stage_name, keep=True) as stage:
                raise Exception()

            path = self.get_stage_path(stage, self.stage_name)
            self.assertTrue(os.path.isdir(path))
        except:
            pass  # ignore here.
