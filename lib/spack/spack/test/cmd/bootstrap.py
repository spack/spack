# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

import pytest

import spack.config
import spack.environment
import spack.main

_bootstrap = spack.main.SpackCommand('bootstrap')


@pytest.mark.parametrize('scope', [
    None, 'site', 'system', 'user'
])
def test_enable_and_disable(mutable_config, scope):
    scope_args = []
    if scope:
        scope_args = ['--scope={0}'.format(scope)]

    _bootstrap('enable', *scope_args)
    assert spack.config.get('bootstrap:enable', scope=scope) is True

    _bootstrap('disable', *scope_args)
    assert spack.config.get('bootstrap:enable', scope=scope) is False


@pytest.mark.parametrize('scope', [
    None, 'site', 'system', 'user'
])
def test_root_get_and_set(mutable_config, scope):
    scope_args, path = [], '/scratch/spack/bootstrap'
    if scope:
        scope_args = ['--scope={0}'.format(scope)]

    _bootstrap('root', path, *scope_args)
    out = _bootstrap('root', *scope_args, output=str)
    assert out.strip() == path


@pytest.mark.parametrize('scopes', [
    ('site',),
    ('system', 'user')
])
def test_reset_in_file_scopes(mutable_config, scopes):
    # Assert files are created in the right scopes
    bootstrap_yaml_files = []
    for s in scopes:
        _bootstrap('disable', '--scope={0}'.format(s))
        scope_path = spack.config.config.scopes[s].path
        bootstrap_yaml = os.path.join(
            scope_path, 'bootstrap.yaml'
        )
        assert os.path.exists(bootstrap_yaml)
        bootstrap_yaml_files.append(bootstrap_yaml)

    _bootstrap('reset', '-y')
    for bootstrap_yaml in bootstrap_yaml_files:
        assert not os.path.exists(bootstrap_yaml)


def test_reset_in_environment(mutable_mock_env_path, mutable_config):
    env = spack.main.SpackCommand('env')
    env('create', 'bootstrap-test')
    current_environment = spack.environment.read('bootstrap-test')

    with current_environment:
        _bootstrap('disable')
        assert spack.config.get('bootstrap:enable') is False
        _bootstrap('reset', '-y')
        # We have no default settings in tests
        assert spack.config.get('bootstrap:enable') is None

    # Check that reset didn't delete the entire file
    spack_yaml = os.path.join(current_environment.path, 'spack.yaml')
    assert os.path.exists(spack_yaml)


def test_reset_in_file_scopes_overwrites_backup_files(mutable_config):
    # Create a bootstrap.yaml with some config
    _bootstrap('disable', '--scope=site')
    scope_path = spack.config.config.scopes['site'].path
    bootstrap_yaml = os.path.join(scope_path, 'bootstrap.yaml')
    assert os.path.exists(bootstrap_yaml)

    # Reset the bootstrap configuration
    _bootstrap('reset', '-y')
    backup_file = bootstrap_yaml + '.bkp'
    assert not os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)

    # Iterate another time
    _bootstrap('disable', '--scope=site')
    assert os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)
    _bootstrap('reset', '-y')
    assert not os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)
