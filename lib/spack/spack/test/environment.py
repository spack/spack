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

from spack import spack_root
from llnl.util.filesystem import join_path
from spack.environment import EnvironmentModifications
from spack.environment import SetEnv, UnsetEnv
from spack.environment import RemovePath, PrependPath, AppendPath
from spack.util.environment import filter_system_paths, filter_system_bin_paths


class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        os.environ['UNSET_ME'] = 'foo'
        os.environ['EMPTY_PATH_LIST'] = ''
        os.environ['PATH_LIST'] = '/path/second:/path/third'
        os.environ['REMOVE_PATH_LIST'] = \
            '/a/b:/duplicate:/a/c:/remove/this:/a/d:/duplicate/:/f/g'

    def tearDown(self):
        pass

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

    def test_filter_system_paths(self):
        filtered = filter_system_paths([
            '/usr/local/Cellar/gcc/5.3.0/lib',
            '/usr/local/lib',
            '/usr/local/include',
            '/usr/local/lib64',
            '/usr/local/opt/some-package/lib',
            '/usr/opt/lib',
            '/lib',
            '/lib64',
            '/include',
            '/opt/some-package/include',
        ])
        self.assertEqual(filtered,
                         ['/usr/local/Cellar/gcc/5.3.0/lib',
                          '/usr/local/opt/some-package/lib',
                          '/usr/opt/lib',
                          '/opt/some-package/include'])

        filtered = filter_system_bin_paths([
            '/usr/local/Cellar/gcc/5.3.0/bin',
            '/usr/local/bin',
            '/usr/local/opt/some-package/bin',
            '/usr/opt/bin',
            '/bin',
            '/opt/some-package/bin',
        ])
        self.assertEqual(filtered,
                         ['/usr/local/bin',
                          '/bin',
                          '/usr/local/Cellar/gcc/5.3.0/bin',
                          '/usr/local/opt/some-package/bin',
                          '/usr/opt/bin',
                          '/opt/some-package/bin'])

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
        self.assertEqual(
            '/path/first:/path/second:/path/third:/path/last',
            os.environ['PATH_LIST']
        )
        self.assertEqual(
            '/path/first:/path/middle:/path/last',
            os.environ['EMPTY_PATH_LIST']
        )
        self.assertEqual(
            '/path/first:/path/middle:/path/last',
            os.environ['NEWLY_CREATED_PATH_LIST']
        )
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

    def test_source_files(self):
        datadir = join_path(spack_root, 'lib', 'spack',
                            'spack', 'test', 'data')
        files = [
            join_path(datadir, 'sourceme_first.sh'),
            join_path(datadir, 'sourceme_second.sh'),
            join_path(datadir, 'sourceme_parameters.sh intel64')
        ]
        env = EnvironmentModifications.from_sourcing_files(*files)
        modifications = env.group_by_name()

        # This is sensitive to the user's environment; can include
        # spurious entries for things like PS1
        #
        # TODO: figure out how to make a bit more robust.
        self.assertTrue(len(modifications) >= 4)

        # Set new variables
        self.assertEqual(len(modifications['NEW_VAR']), 1)
        self.assertTrue(isinstance(modifications['NEW_VAR'][0], SetEnv))
        self.assertEqual(modifications['NEW_VAR'][0].value, 'new')

        self.assertEqual(len(modifications['FOO']), 1)
        self.assertTrue(isinstance(modifications['FOO'][0], SetEnv))
        self.assertEqual(modifications['FOO'][0].value, 'intel64')

        # Unset variables
        self.assertEqual(len(modifications['EMPTY_PATH_LIST']), 1)
        self.assertTrue(isinstance(
            modifications['EMPTY_PATH_LIST'][0], UnsetEnv))
        # Modified variables
        self.assertEqual(len(modifications['UNSET_ME']), 1)
        self.assertTrue(isinstance(modifications['UNSET_ME'][0], SetEnv))
        self.assertEqual(modifications['UNSET_ME'][0].value, 'overridden')

        self.assertEqual(len(modifications['PATH_LIST']), 3)
        self.assertTrue(
            isinstance(modifications['PATH_LIST'][0], RemovePath)
        )
        self.assertEqual(modifications['PATH_LIST'][0].value, '/path/third')
        self.assertTrue(
            isinstance(modifications['PATH_LIST'][1], AppendPath)
        )
        self.assertEqual(modifications['PATH_LIST'][1].value, '/path/fourth')
        self.assertTrue(
            isinstance(modifications['PATH_LIST'][2], PrependPath)
        )
        self.assertEqual(modifications['PATH_LIST'][2].value, '/path/first')
