# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    def test_parent_dir(self, stage):
        """Test copying to from a parent directory."""

        # Make sure we get the right error if we try to copy a parent into
        # a descendent directory.
        with pytest.raises(ValueError, matches="Cannot copy"):
            with fs.working_dir(str(stage)):
                fs.copy_tree('source', 'source/sub/directory')

        # Only point with this check is to make sure we don't try to perform
        # the copy.
        with pytest.raises(IOError, matches="No such file or directory"):
            with fs.working_dir(str(stage)):
                fs.copy_tree('foo/ba', 'foo/bar')

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


def test_paths_containing_libs(dirs_with_libfiles):
    lib_to_dirs, all_dirs = dirs_with_libfiles

    assert (set(fs.paths_containing_libs(all_dirs, ['libgfortran'])) ==
            set(lib_to_dirs['libgfortran']))

    assert (set(fs.paths_containing_libs(all_dirs, ['libirc'])) ==
            set(lib_to_dirs['libirc']))


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


@pytest.mark.regression('10601')
@pytest.mark.regression('10603')
def test_recursive_search_of_headers_from_prefix(
        installation_dir_with_headers
):
    # Try to inspect recursively from <prefix> and ensure we don't get
    # subdirectories of the '<prefix>/include' path
    prefix = str(installation_dir_with_headers)
    header_list = fs.find_all_headers(prefix)

    # Check that the header files we expect are all listed
    assert os.path.join(prefix, 'include', 'ex3.h') in header_list
    assert os.path.join(prefix, 'include', 'boost', 'ex3.h') in header_list
    assert os.path.join(prefix, 'path', 'to', 'ex1.h') in header_list
    assert os.path.join(prefix, 'path', 'to', 'subdir', 'ex2.h') in header_list

    # Check that when computing directories we exclude <prefix>/include/boost
    include_dirs = header_list.directories
    assert os.path.join(prefix, 'include') in include_dirs
    assert os.path.join(prefix, 'include', 'boost') not in include_dirs
    assert os.path.join(prefix, 'path', 'to') in include_dirs
    assert os.path.join(prefix, 'path', 'to', 'subdir') in include_dirs


@pytest.mark.parametrize('list_of_headers,expected_directories', [
    (['/pfx/include/foo.h', '/pfx/include/subdir/foo.h'], ['/pfx/include']),
    (['/pfx/include/foo.h', '/pfx/subdir/foo.h'],
     ['/pfx/include', '/pfx/subdir']),
    (['/pfx/include/subdir/foo.h', '/pfx/subdir/foo.h'],
     ['/pfx/include', '/pfx/subdir'])
])
def test_computation_of_header_directories(
        list_of_headers, expected_directories
):
    hl = fs.HeaderList(list_of_headers)
    assert hl.directories == expected_directories


def test_headers_directory_setter():
    hl = fs.HeaderList(
        ['/pfx/include/subdir/foo.h', '/pfx/include/subdir/bar.h']
    )

    # Set directories using a list
    hl.directories = ['/pfx/include/subdir']
    assert hl.directories == ['/pfx/include/subdir']

    # If it's a single directory it's fine to not wrap it into a list
    # when setting the property
    hl.directories = '/pfx/include/subdir'
    assert hl.directories == ['/pfx/include/subdir']

    # Paths are normalized, so it doesn't matter how many backslashes etc.
    # are present in the original directory being used
    hl.directories = '/pfx/include//subdir/'
    assert hl.directories == ['/pfx/include/subdir']

    # Setting an empty list is allowed and returns an empty list
    hl.directories = []
    assert hl.directories == []

    # Setting directories to None also returns an empty list
    hl.directories = None
    assert hl.directories == []
