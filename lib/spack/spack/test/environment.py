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

    def test_set_env(self):
        env = EnvironmentModifications()
        env.set_env('A', 'dummy value')
        env.set_env('B', 3)
        env.apply_modifications()
        self.assertEqual('dummy value', os.environ['A'])
        self.assertEqual(str(3), os.environ['B'])

    def test_unset_env(self):
        env = EnvironmentModifications()
        self.assertEqual('foo', os.environ['UNSET_ME'])
        env.unset_env('UNSET_ME')
        env.apply_modifications()
        self.assertRaises(KeyError, os.environ.__getitem__, 'UNSET_ME')

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
        env.set_env('A', 'dummy value', who='Pkg1')
        for x in env:
            assert 'who' in x.args
        env.apply_modifications()
        self.assertEqual('dummy value', os.environ['A'])

    def test_extend(self):
        env = EnvironmentModifications()
        env.set_env('A', 'dummy value')
        env.set_env('B', 3)
        copy_construct = EnvironmentModifications(env)
        self.assertEqual(len(copy_construct), 2)
        for x, y in zip(env, copy_construct):
            assert x is y
