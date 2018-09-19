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
import os

import pytest
from llnl.util.filesystem import working_dir, mkdirp, touchp
from llnl.util.link_tree import LinkTree
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


def check_file_link(filename):
    assert os.path.isfile(filename)
    assert os.path.islink(filename)


def check_dir(filename):
    assert os.path.isdir(filename)


def test_merge_to_new_directory(stage, link_tree):
    with working_dir(stage.path):
        link_tree.merge('dest')

        check_file_link('dest/1')
        check_file_link('dest/a/b/2')
        check_file_link('dest/a/b/3')
        check_file_link('dest/c/4')
        check_file_link('dest/c/d/5')
        check_file_link('dest/c/d/6')
        check_file_link('dest/c/d/e/7')

        link_tree.unmerge('dest')

        assert not os.path.exists('dest')


def test_merge_to_existing_directory(stage, link_tree):
    with working_dir(stage.path):

        touchp('dest/x')
        touchp('dest/a/b/y')

        link_tree.merge('dest')

        check_file_link('dest/1')
        check_file_link('dest/a/b/2')
        check_file_link('dest/a/b/3')
        check_file_link('dest/c/4')
        check_file_link('dest/c/d/5')
        check_file_link('dest/c/d/6')
        check_file_link('dest/c/d/e/7')

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
