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
import os
import unittest

from llnl.util.filesystem import *
from llnl.util.link_tree import LinkTree

from spack.stage import Stage


class LinkTreeTest(unittest.TestCase):
    """Tests Spack's LinkTree class."""

    def setUp(self):
        self.stage = Stage('link-tree-test')
        self.stage.create()

        with working_dir(self.stage.path):
            touchp('source/1')
            touchp('source/a/b/2')
            touchp('source/a/b/3')
            touchp('source/c/4')
            touchp('source/c/d/5')
            touchp('source/c/d/6')
            touchp('source/c/d/e/7')

        source_path = os.path.join(self.stage.path, 'source')
        self.link_tree = LinkTree(source_path)

    def tearDown(self):
        self.stage.destroy()


    def check_file_link(self, filename):
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.path.islink(filename))


    def check_dir(self, filename):
        self.assertTrue(os.path.isdir(filename))


    def test_merge_to_new_directory(self):
        with working_dir(self.stage.path):
            self.link_tree.merge('dest')

            self.check_file_link('dest/1')
            self.check_file_link('dest/a/b/2')
            self.check_file_link('dest/a/b/3')
            self.check_file_link('dest/c/4')
            self.check_file_link('dest/c/d/5')
            self.check_file_link('dest/c/d/6')
            self.check_file_link('dest/c/d/e/7')

            self.link_tree.unmerge('dest')

            self.assertFalse(os.path.exists('dest'))


    def test_merge_to_existing_directory(self):
        with working_dir(self.stage.path):

            touchp('dest/x')
            touchp('dest/a/b/y')

            self.link_tree.merge('dest')

            self.check_file_link('dest/1')
            self.check_file_link('dest/a/b/2')
            self.check_file_link('dest/a/b/3')
            self.check_file_link('dest/c/4')
            self.check_file_link('dest/c/d/5')
            self.check_file_link('dest/c/d/6')
            self.check_file_link('dest/c/d/e/7')

            self.assertTrue(os.path.isfile('dest/x'))
            self.assertTrue(os.path.isfile('dest/a/b/y'))

            self.link_tree.unmerge('dest')

            self.assertTrue(os.path.isfile('dest/x'))
            self.assertTrue(os.path.isfile('dest/a/b/y'))

            self.assertFalse(os.path.isfile('dest/1'))
            self.assertFalse(os.path.isfile('dest/a/b/2'))
            self.assertFalse(os.path.isfile('dest/a/b/3'))
            self.assertFalse(os.path.isfile('dest/c/4'))
            self.assertFalse(os.path.isfile('dest/c/d/5'))
            self.assertFalse(os.path.isfile('dest/c/d/6'))
            self.assertFalse(os.path.isfile('dest/c/d/e/7'))


    def test_merge_with_empty_directories(self):
        with working_dir(self.stage.path):
            mkdirp('dest/f/g')
            mkdirp('dest/a/b/h')

            self.link_tree.merge('dest')
            self.link_tree.unmerge('dest')

            self.assertFalse(os.path.exists('dest/1'))
            self.assertFalse(os.path.exists('dest/a/b/2'))
            self.assertFalse(os.path.exists('dest/a/b/3'))
            self.assertFalse(os.path.exists('dest/c/4'))
            self.assertFalse(os.path.exists('dest/c/d/5'))
            self.assertFalse(os.path.exists('dest/c/d/6'))
            self.assertFalse(os.path.exists('dest/c/d/e/7'))

            self.assertTrue(os.path.isdir('dest/a/b/h'))
            self.assertTrue(os.path.isdir('dest/f/g'))


    def test_ignore(self):
        with working_dir(self.stage.path):
            touchp('source/.spec')
            touchp('dest/.spec')

            self.link_tree.merge('dest', ignore=lambda x: x == '.spec')
            self.link_tree.unmerge('dest', ignore=lambda x: x == '.spec')

            self.assertFalse(os.path.exists('dest/1'))
            self.assertFalse(os.path.exists('dest/a'))
            self.assertFalse(os.path.exists('dest/c'))

            self.assertTrue(os.path.isfile('source/.spec'))
            self.assertTrue(os.path.isfile('dest/.spec'))
