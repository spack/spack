# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.filesystem import mkdirp, touchp, working_dir
from llnl.util.link_tree import LinkTree
from llnl.util.symlink import islink

from spack.stage import Stage


@pytest.fixture()
def stage():
    """Creates a stage with the directory structure for the tests."""
    s = Stage('link-tree-test')
    s.create()

    with working_dir(s.path):
        touchp('source/1')
        touchp('source/a/b/2')
        touchp('source/a/b/3')
        touchp('source/c/4')
        touchp('source/c/d/5')
        touchp('source/c/d/6')
        touchp('source/c/d/e/7')

    yield s

    s.destroy()


@pytest.fixture()
def link_tree(stage):
    """Return a properly initialized LinkTree instance."""
    source_path = os.path.join(stage.path, 'source')
    return LinkTree(source_path)


def check_file_link(filename, expected_target):
    assert os.path.isfile(filename)
    assert islink(filename)
    assert (os.path.abspath(os.path.realpath(filename)) ==
            os.path.abspath(expected_target))


def check_dir(filename):
    assert os.path.isdir(filename)


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_merge_to_new_directory(stage, link_tree):
    with working_dir(stage.path):
        link_tree.merge('dest')

        check_file_link('dest/1',       'source/1')
        check_file_link('dest/a/b/2',   'source/a/b/2')
        check_file_link('dest/a/b/3',   'source/a/b/3')
        check_file_link('dest/c/4',     'source/c/4')
        check_file_link('dest/c/d/5',   'source/c/d/5')
        check_file_link('dest/c/d/6',   'source/c/d/6')
        check_file_link('dest/c/d/e/7', 'source/c/d/e/7')

        assert os.path.isabs(os.readlink('dest/1'))
        assert os.path.isabs(os.readlink('dest/a/b/2'))
        assert os.path.isabs(os.readlink('dest/a/b/3'))
        assert os.path.isabs(os.readlink('dest/c/4'))
        assert os.path.isabs(os.readlink('dest/c/d/5'))
        assert os.path.isabs(os.readlink('dest/c/d/6'))
        assert os.path.isabs(os.readlink('dest/c/d/e/7'))

        link_tree.unmerge('dest')

        assert not os.path.exists('dest')


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_merge_to_new_directory_relative(stage, link_tree):
    with working_dir(stage.path):
        link_tree.merge('dest', relative=True)

        check_file_link('dest/1',       'source/1')
        check_file_link('dest/a/b/2',   'source/a/b/2')
        check_file_link('dest/a/b/3',   'source/a/b/3')
        check_file_link('dest/c/4',     'source/c/4')
        check_file_link('dest/c/d/5',   'source/c/d/5')
        check_file_link('dest/c/d/6',   'source/c/d/6')
        check_file_link('dest/c/d/e/7', 'source/c/d/e/7')

        assert not os.path.isabs(os.readlink('dest/1'))
        assert not os.path.isabs(os.readlink('dest/a/b/2'))
        assert not os.path.isabs(os.readlink('dest/a/b/3'))
        assert not os.path.isabs(os.readlink('dest/c/4'))
        assert not os.path.isabs(os.readlink('dest/c/d/5'))
        assert not os.path.isabs(os.readlink('dest/c/d/6'))
        assert not os.path.isabs(os.readlink('dest/c/d/e/7'))

        link_tree.unmerge('dest')

        assert not os.path.exists('dest')


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_merge_to_existing_directory(stage, link_tree):
    with working_dir(stage.path):

        touchp('dest/x')
        touchp('dest/a/b/y')

        link_tree.merge('dest')

        check_file_link('dest/1',       'source/1')
        check_file_link('dest/a/b/2',   'source/a/b/2')
        check_file_link('dest/a/b/3',   'source/a/b/3')
        check_file_link('dest/c/4',     'source/c/4')
        check_file_link('dest/c/d/5',   'source/c/d/5')
        check_file_link('dest/c/d/6',   'source/c/d/6')
        check_file_link('dest/c/d/e/7', 'source/c/d/e/7')

        assert os.path.isfile('dest/x')
        assert os.path.isfile('dest/a/b/y')

        link_tree.unmerge('dest')

        assert os.path.isfile('dest/x')
        assert os.path.isfile('dest/a/b/y')

        assert not os.path.isfile('dest/1')
        assert not os.path.isfile('dest/a/b/2')
        assert not os.path.isfile('dest/a/b/3')
        assert not os.path.isfile('dest/c/4')
        assert not os.path.isfile('dest/c/d/5')
        assert not os.path.isfile('dest/c/d/6')
        assert not os.path.isfile('dest/c/d/e/7')


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_merge_with_empty_directories(stage, link_tree):
    with working_dir(stage.path):
        mkdirp('dest/f/g')
        mkdirp('dest/a/b/h')

        link_tree.merge('dest')
        link_tree.unmerge('dest')

        assert not os.path.exists('dest/1')
        assert not os.path.exists('dest/a/b/2')
        assert not os.path.exists('dest/a/b/3')
        assert not os.path.exists('dest/c/4')
        assert not os.path.exists('dest/c/d/5')
        assert not os.path.exists('dest/c/d/6')
        assert not os.path.exists('dest/c/d/e/7')

        assert os.path.isdir('dest/a/b/h')
        assert os.path.isdir('dest/f/g')


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_ignore(stage, link_tree):
    with working_dir(stage.path):
        touchp('source/.spec')
        touchp('dest/.spec')

        link_tree.merge('dest', ignore=lambda x: x == '.spec')
        link_tree.unmerge('dest', ignore=lambda x: x == '.spec')

        assert not os.path.exists('dest/1')
        assert not os.path.exists('dest/a')
        assert not os.path.exists('dest/c')

        assert os.path.isfile('source/.spec')
        assert os.path.isfile('dest/.spec')
