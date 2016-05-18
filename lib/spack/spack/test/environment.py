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
import unittest
import os
from spack.environment import EnvironmentModifications


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        os.environ.clear()
        os.environ['UNSET_ME'] = 'foo'
        os.environ['EMPTY_PATH_LIST'] = ''
        os.environ['PATH_LIST'] = '/path/second:/path/third'
        os.environ['REMOVE_PATH_LIST'] = '/a/b:/duplicate:/a/c:/remove/this:/a/d:/duplicate/:/f/g'

    def test_set(self):
        env = EnvironmentModifications()
        env.set('A', 'dummy value')
        env.set('B', 3)
        env.apply_modifications()
        self.assertEqual('dummy value', os.environ['A'])
        self.assertEqual(str(3), os.environ['B'])

    def test_unset(self):
        env = EnvironmentModifications()
        self.assertEqual('foo', os.environ['UNSET_ME'])
        env.unset('UNSET_ME')
        env.apply_modifications()
        self.assertRaises(KeyError, os.environ.__getitem__, 'UNSET_ME')

    def test_set_path(self):
        env = EnvironmentModifications()
        env.set_path('A', ['foo', 'bar', 'baz'])
        env.apply_modifications()
        self.assertEqual('foo:bar:baz', os.environ['A'])

    def test_path_manipulation(self):
        env = EnvironmentModifications()

        env.append_path('PATH_LIST', '/path/last')
        env.prepend_path('PATH_LIST', '/path/first')

        env.append_path('EMPTY_PATH_LIST', '/path/middle')
        env.append_path('EMPTY_PATH_LIST', '/path/last')
        env.prepend_path('EMPTY_PATH_LIST', '/path/first')

        env.append_path('NEWLY_CREATED_PATH_LIST', '/path/middle')
        env.append_path('NEWLY_CREATED_PATH_LIST', '/path/last')
        env.prepend_path('NEWLY_CREATED_PATH_LIST', '/path/first')

        env.remove_path('REMOVE_PATH_LIST', '/remove/this')
        env.remove_path('REMOVE_PATH_LIST', '/duplicate/')

        env.apply_modifications()
        self.assertEqual('/path/first:/path/second:/path/third:/path/last', os.environ['PATH_LIST'])
        self.assertEqual('/path/first:/path/middle:/path/last', os.environ['EMPTY_PATH_LIST'])
        self.assertEqual('/path/first:/path/middle:/path/last', os.environ['NEWLY_CREATED_PATH_LIST'])
        self.assertEqual('/a/b:/a/c:/a/d:/f/g', os.environ['REMOVE_PATH_LIST'])

    def test_extra_arguments(self):
        env = EnvironmentModifications()
        env.set('A', 'dummy value', who='Pkg1')
        for x in env:
            assert 'who' in x.args
        env.apply_modifications()
        self.assertEqual('dummy value', os.environ['A'])

    def test_extend(self):
        env = EnvironmentModifications()
        env.set('A', 'dummy value')
        env.set('B', 3)
        copy_construct = EnvironmentModifications(env)
        self.assertEqual(len(copy_construct), 2)
        for x, y in zip(env, copy_construct):
            assert x is y
