# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
import os
import os.path

from six import StringIO

from llnl.util.filesystem import mkdirp

import spack.config
import spack.environment
from spack.cmd.env import _env_create


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures(
    'mutable_mock_env_path', 'config')


@pytest.fixture()
def write_custom_scope(tmpdir):
    """Returns a function that writes a custom scope."""
    def _write(scope_name, **sections):
        scopedir = os.path.join(str(tmpdir), scope_name)
        mkdirp(scopedir)
        for section, content in sections.items():
            with open(os.path.join(scopedir, section + '.yaml'), 'w') as f:
                f.write(content)
        return scopedir
    return _write


def in_config_scopes(needle):
    """Returns true if needle is found in current config scopes names"""
    return any(needle in n for n in spack.config.config.scopes.keys())


def test_config_include_section(write_custom_scope):
    """Test include.yaml config including another config scope"""
    scopea = write_custom_scope(
        'scopea', include="""\
include:
  - ../scopeb
""")
    write_custom_scope(
        'scopeb', packages="""\
packages:
  mpileaks:
    version: [2.2]
""")

    # Sanity check
    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' not in packages

    configscope = spack.config.ConfigScope('scopea', scopea)
    spack.config.config.push_scope(configscope)

    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' in packages

    spack.config.config.remove_scope(configscope.name)

    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' not in packages


def test_config_include_variable(write_custom_scope):
    """Test env variable in included path"""
    scopea = write_custom_scope(
        'scopea', include="""\
include:
  - ${TEST_ENV_VAR}/scopeb
""")
    scopeb = write_custom_scope(
        'scopeb', packages="""\
packages:
  mpileaks:
    version: [2.2]
""")
    os.environ['TEST_ENV_VAR'] = str(os.path.dirname(scopeb))

    # Sanity check
    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' not in packages

    configscope = spack.config.ConfigScope('scopea', scopea)
    spack.config.config.push_scope(configscope)

    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' in packages

    spack.config.config.remove_scope(configscope.name)

    os.environ.pop('TEST_ENV_VAR')


def test_config_include_in_env_configscope(write_custom_scope):
    """Test a spack-env including a config scope"""
    included = write_custom_scope(
        'included-config', packages="""\
packages:
  mpileaks:
    version: [2.2]
""")

    test_config = """\
env:
  include:
  - %s
  specs:
  - mpileaks
""" % str(included)
    _env_create('test', StringIO(test_config))
    e = spack.environment.read('test')

    # Sanity check
    assert not in_config_scopes('included-config')

    with e:
        assert in_config_scopes('included-config')

    assert not in_config_scopes('included-config')


def test_config_include_in_env_singlefile(write_custom_scope):
    """Test a spack-env including a "single file" config"""
    test_config = """\
env:
  include:
  - ./included-config.yaml
  specs:
  - mpileaks
"""
    _env_create('test', StringIO(test_config))
    e = spack.environment.read('test')

    with open(os.path.join(e.path, 'included-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    # Sanity check
    assert not in_config_scopes('included-config')

    with e:
        assert in_config_scopes('included-config')

    assert not in_config_scopes('included-config')


def test_config_include_multiple_levels(write_custom_scope):
    """Test multiple levels of includes"""
    scopes = []
    for i in range(3):
        scope = write_custom_scope(
            'testscope-%d' % i, include="""\
include:
  - ../testscope-%d
""" % (i + 1))
        scopes.append(scope)
    i += 1
    write_custom_scope(
        'testscope-%d' % i, packages="""\
packages:
  mpileaks:
    version: [2.2]
""")

    # Sanity check
    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' not in packages

    configscope = spack.config.ConfigScope('testscope-0', scopes[0])
    spack.config.config.push_scope(configscope)

    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' in packages

    spack.config.config.remove_scope(configscope.name)

    # All "testscope-%d" must have been removed
    assert not in_config_scopes('testscope-')

    packages = spack.config.config.get_config('packages')
    assert 'mpileaks' not in packages
