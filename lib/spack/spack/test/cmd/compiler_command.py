# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import os
import os.path
import platform

import spack.main

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


@pytest.mark.regression('11678')
@pytest.mark.requires_executables('/usr/bin/gcc')
def test_compiler_find_without_paths(no_compilers_yaml):
    output = compiler('find', '--scope=site')

    if platform.system() == 'Darwin':
        # /usr/bin/gcc is secretly a clang compiler on Darwin
        assert 'clang' in output
    else:
        assert 'gcc' in output
