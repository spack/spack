# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.config
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
