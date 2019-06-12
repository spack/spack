# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import os
import os.path

import spack.main
import spack.compilers

compiler = spack.main.SpackCommand('compiler')


@pytest.fixture
def no_compilers_yaml(mutable_config, monkeypatch):
    """Creates a temporary configuration without compilers.yaml"""

    for scope, local_config in mutable_config.scopes.items():
        compilers_yaml = os.path.join(
            local_config.path, scope, 'compilers.yaml'
        )
        if os.path.exists(compilers_yaml):
            os.remove(compilers_yaml)

    # This is essential, otherwise the cache will create weird side effects
    # that will compromise subsequent tests
    monkeypatch.setattr(spack.compilers, '_cache_config_file', [])


@pytest.mark.regression('11678')
@pytest.mark.requires_executables('/usr/bin/gcc')
def test_compiler_find_without_paths(no_compilers_yaml):
    output = compiler('find', '--scope=site')

    assert 'gcc' in output
