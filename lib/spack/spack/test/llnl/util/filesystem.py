##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
"""Tests for ``llnl/util/filesystem.py``"""

import llnl.util.filesystem as fs
import os
import stat
import pytest


@pytest.fixture()
def stage(tmpdir_factory):
    """Creates a stage with the directory structure for the tests."""

    s = tmpdir_factory.mktemp('filesystem_test')

    with s.as_cwd():
        # Create source file hierarchy
        fs.touchp('source/1')
        fs.touchp('source/a/b/2')
        fs.touchp('source/a/b/3')
        fs.touchp('source/c/4')
        fs.touchp('source/c/d/5')
        fs.touchp('source/c/d/6')
        fs.touchp('source/c/d/e/7')

        # Create symlinks
        os.symlink(os.path.abspath('source/1'), 'source/2')
        os.symlink('b/2', 'source/a/b2')
        os.symlink('a/b', 'source/f')

        # Create destination directory
        fs.mkdirp('dest')

    yield s


class TestCopy:
    """Tests for ``filesystem.copy``"""

    def test_file_dest(self, stage):
        """Test using a filename as the destination."""

        with fs.working_dir(str(stage)):
            fs.copy('source/1', 'dest/1')

            assert os.path.exists('dest/1')

    def test_dir_dest(self, stage):
        """Test using a directory as the destination."""

        with fs.working_dir(str(stage)):
            fs.copy('source/1', 'dest')

            assert os.path.exists('dest/1')


def check_added_exe_permissions(src, dst):
    src_mode = os.stat(src).st_mode
    dst_mode = os.stat(dst).st_mode
    for perm in [stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH]:
        if src_mode & perm:
            assert dst_mode & perm


class TestInstall:
    """Tests for ``filesystem.install``"""

    def test_file_dest(self, stage):
        """Test using a filename as the destination."""

        with fs.working_dir(str(stage)):
            fs.install('source/1', 'dest/1')

            assert os.path.exists('dest/1')
            check_added_exe_permissions('source/1', 'dest/1')

    def test_dir_dest(self, stage):
        """Test using a directory as the destination."""

        with fs.working_dir(str(stage)):
            fs.install('source/1', 'dest')

            assert os.path.exists('dest/1')
            check_added_exe_permissions('source/1', 'dest/1')


class TestCopyTree:
    """Tests for ``filesystem.copy_tree``"""

    def test_existing_dir(self, stage):
        """Test copying to an existing directory."""

        with fs.working_dir(str(stage)):
            fs.copy_tree('source', 'dest')

            assert os.path.exists('dest/a/b/2')

    def test_non_existing_dir(self, stage):
        """Test copying to a non-existing directory."""

        with fs.working_dir(str(stage)):
            fs.copy_tree('source', 'dest/sub/directory')

            assert os.path.exists('dest/sub/directory/a/b/2')

    def test_symlinks_true(self, stage):
        """Test copying with symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.copy_tree('source', 'dest', symlinks=True)

            assert os.path.exists('dest/2')
            assert os.path.islink('dest/2')

            assert os.path.exists('dest/a/b2')
            with fs.working_dir('dest/a'):
                assert os.path.exists(os.readlink('b2'))

            assert (os.path.realpath('dest/f/2') ==
                    os.path.abspath('dest/a/b/2'))
            assert os.path.realpath('dest/2') == os.path.abspath('dest/1')

    def test_symlinks_true_ignore(self, stage):
        """Test copying when specifying relative paths that should be ignored
        """
        with fs.working_dir(str(stage)):
            ignore = lambda p: p in ['c/d/e', 'a']
            fs.copy_tree('source', 'dest', symlinks=True, ignore=ignore)
            assert not os.path.exists('dest/a')
            assert os.path.exists('dest/c/d')
            assert not os.path.exists('dest/c/d/e')

    def test_symlinks_false(self, stage):
        """Test copying without symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.copy_tree('source', 'dest', symlinks=False)

            assert os.path.exists('dest/2')
            assert not os.path.islink('dest/2')


class TestInstallTree:
    """Tests for ``filesystem.install_tree``"""

    def test_existing_dir(self, stage):
        """Test installing to an existing directory."""

        with fs.working_dir(str(stage)):
            fs.install_tree('source', 'dest')

            assert os.path.exists('dest/a/b/2')

    def test_non_existing_dir(self, stage):
        """Test installing to a non-existing directory."""

        with fs.working_dir(str(stage)):
            fs.install_tree('source', 'dest/sub/directory')

            assert os.path.exists('dest/sub/directory/a/b/2')

    def test_symlinks_true(self, stage):
        """Test installing with symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.install_tree('source', 'dest', symlinks=True)

            assert os.path.exists('dest/2')
            assert os.path.islink('dest/2')

    def test_symlinks_false(self, stage):
        """Test installing without symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.install_tree('source', 'dest', symlinks=False)

            assert os.path.exists('dest/2')
            assert not os.path.islink('dest/2')


def test_move_transaction_commit(tmpdir):

    fake_library = tmpdir.mkdir('lib').join('libfoo.so')
    fake_library.write('Just some fake content.')

    old_md5 = fs.hash_directory(str(tmpdir))

    with fs.replace_directory_transaction(str(tmpdir.join('lib'))):
        fake_library = tmpdir.mkdir('lib').join('libfoo.so')
        fake_library.write('Other content.')
        new_md5 = fs.hash_directory(str(tmpdir))

    assert old_md5 != fs.hash_directory(str(tmpdir))
    assert new_md5 == fs.hash_directory(str(tmpdir))


def test_move_transaction_rollback(tmpdir):

    fake_library = tmpdir.mkdir('lib').join('libfoo.so')
    fake_library.write('Just some fake content.')

    h = fs.hash_directory(str(tmpdir))

    try:
        with fs.replace_directory_transaction(str(tmpdir.join('lib'))):
            assert h != fs.hash_directory(str(tmpdir))
            fake_library = tmpdir.mkdir('lib').join('libfoo.so')
            fake_library.write('Other content.')
            raise RuntimeError('')
    except RuntimeError:
        pass

    assert h == fs.hash_directory(str(tmpdir))
