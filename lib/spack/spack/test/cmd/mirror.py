# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os

from spack.main import SpackCommand, SpackCommandError
import spack.environment as ev
import spack.config

mirror = SpackCommand('mirror')
env = SpackCommand('env')
add = SpackCommand('add')
concretize = SpackCommand('concretize')


def curry_scope_arg(command, index, scope_name, scope_arg='--scope'):
    return lambda *args, **kwargs: (
        command(args[0], scope_arg, scope_name, *args[1:], **kwargs))


@pytest.fixture
def tmp_scope():
    """Creates a temporary configuration scope"""

    base_name = 'internal-testing-scope'
    current_overrides = set(
        x.name for x in
        spack.config.config.matching_scopes(r'^{0}'.format(base_name)))

    num_overrides = 0
    scope_name = base_name
    while scope_name in current_overrides:
        scope_name = '{0}{1}'.format(base_name, num_overrides)
        num_overrides += 1

    with spack.config.override(spack.config.InternalConfigScope(scope_name)):
        yield scope_name


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('8083')
def test_regression_8083(tmpdir, capfd, mock_packages, mock_fetch, config):
    with capfd.disabled():
        output = mirror('create', '-d', str(tmpdir), 'externaltool')
    assert 'Skipping' in output
    assert 'as it is an external spec' in output


@pytest.mark.regression('12345')
def test_mirror_from_env(tmpdir, mock_packages, mock_fetch, config,
                         mutable_mock_env_path):
    mirror_dir = str(tmpdir)
    env_name = 'test'

    env('create', env_name)
    with ev.read(env_name):
        add('trivial-install-test-package')
        add('git-test')
        concretize()
        with spack.config.override('config:checksum', False):
            mirror('create', '-d', mirror_dir, '--all')

    e = ev.read(env_name)
    assert set(os.listdir(mirror_dir)) == set([s.name for s in e.user_specs])
    for spec in e.specs_by_hash.values():
        mirror_res = os.listdir(os.path.join(mirror_dir, spec.name))
        expected = ['%s.tar.gz' % spec.format('{name}-{version}')]
        assert mirror_res == expected


def test_mirror_crud(tmp_scope):
    mirror_ = curry_scope_arg(mirror, 1, tmp_scope)

    mirror_('add', 'mirror', 'http://spack.io')
    output = mirror_('remove', 'mirror')
    assert 'Removed mirror' in output

    output = mirror_('add', 'mirror', 'http://spack.io')

    # no-op
    output = mirror_('set-url', 'mirror', 'http://spack.io')
    assert 'Url already set' in output

    output = mirror_('set-url', '--push', 'mirror', 's3://spack-public')
    assert 'Changed (push) url' in output

    # no-op
    output = mirror_('set-url', '--push', 'mirror', 's3://spack-public')
    assert 'Url already set' in output

    output = mirror_('remove', 'mirror')
    assert 'Removed mirror' in output

    output = mirror_('list')
    assert 'No mirrors configured' in output


def test_mirror_nonexisting(tmp_scope):
    mirror_ = curry_scope_arg(mirror, 1, tmp_scope)

    with pytest.raises(SpackCommandError):
        mirror_('remove', 'not-a-mirror')

    with pytest.raises(SpackCommandError):
        mirror_('set-url', 'not-a-mirror', 'http://spack.io')


def test_mirror_name_collision(tmp_scope):
    mirror_ = curry_scope_arg(mirror, 1, tmp_scope)

    mirror_('add', 'first', '1')

    with pytest.raises(SpackCommandError):
        mirror_('add', 'first', '1')
