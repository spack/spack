# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import os

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


@pytest.mark.regression('11678,13138')
def test_compiler_find_without_paths(no_compilers_yaml, working_env, tmpdir):
    with tmpdir.as_cwd():
        with open('gcc', 'w') as f:
            f.write("""\
#!/bin/bash
echo "0.0.0"
""")
        os.chmod('gcc', 0o700)

    os.environ['PATH'] = str(tmpdir)
    output = compiler('find', '--scope=site')

    assert 'gcc' in output
