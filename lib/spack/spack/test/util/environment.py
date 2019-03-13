# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's environment utility functions."""
import os
import spack.util.environment as envutil


def test_is_system_path():
    assert(envutil.is_system_path('/usr/bin'))
    assert(not envutil.is_system_path('/nonsense_path/bin'))


test_paths = ['/usr/bin',
              '/nonsense_path/lib',
              '/usr/local/lib',
              '/bin',
              '/nonsense_path/extra/bin',
              '/usr/lib64']


def test_filter_system_paths():
    expected = [p for p in test_paths if p.startswith('/nonsense_path')]
    filtered = envutil.filter_system_paths(test_paths)
    assert(expected == filtered)


def test_system_paths():
    expected = [p for p in test_paths if not p.startswith('/nonsense_path')]
    filtered = envutil.system_paths(test_paths)
    assert(expected == filtered)


def deprioritize_system_paths():
    expected = [p for p in test_paths if p.startswith('/nonsense_path')]
    expected.extend([p for p in test_paths
                     if not p.startswith('/nonsense_path')])
    filtered = envutil.deprioritize_system_paths(test_paths)
    assert(expected == filtered)


def test_prune_duplicate_paths():
    test_paths = ['/a/b', '/a/c', '/a/b', '/a/a', '/a/c', '/a/a/..']
    expected = ['/a/b', '/a/c', '/a/a', '/a/a/..']
    assert(expected == envutil.prune_duplicate_paths(test_paths))


def test_get_path():
    os.environ['TEST_ENV_VAR'] = '/a:/b:/c/d'
    expected = ['/a', '/b', '/c/d']
    assert(envutil.get_path('TEST_ENV_VAR') == expected)
    del os.environ['TEST_ENV_VAR']


def test_env_flag():
    assert(not envutil.env_flag('TEST_NO_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = '1'
    assert(envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'TRUE'
    assert(envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'True'
    assert(envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'TRue'
    assert(envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'true'
    assert(envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = '27'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = '-2.3'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = '0'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'False'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'false'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    os.environ['TEST_ENV_VAR'] = 'garbage'
    assert(not envutil.env_flag('TEST_ENV_VAR'))
    del os.environ['TEST_ENV_VAR']


def test_path_set():
    envutil.path_set('TEST_ENV_VAR', ['/a', '/a/b', '/a/a'])
    assert(os.environ['TEST_ENV_VAR'] == '/a:/a/b:/a/a')
    del os.environ['TEST_ENV_VAR']


def test_path_put_first():
    envutil.path_set('TEST_ENV_VAR', test_paths)
    expected = ['/usr/bin', '/new_nonsense_path/a/b']
    expected.extend([p for p in test_paths if p != '/usr/bin'])
    envutil.path_put_first('TEST_ENV_VAR', expected)
    assert(envutil.get_path('TEST_ENV_VAR') == expected)


def test_dump_environment(tmpdir):
    test_paths = '/a:/b/x:/b/c'
    os.environ['TEST_ENV_VAR'] = test_paths
    dumpfile_path = str(tmpdir.join('envdump.txt'))
    envutil.dump_environment(dumpfile_path)
    with open(dumpfile_path, 'r') as dumpfile:
        assert('TEST_ENV_VAR={0}; export TEST_ENV_VAR\n'.format(test_paths)
               in list(dumpfile))
    del os.environ['TEST_ENV_VAR']
