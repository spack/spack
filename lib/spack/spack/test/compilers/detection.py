# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test detection of compiler version"""
import os.path

import pytest
import os

import spack.paths
import spack.repo
import spack.util.spack_yaml as syaml

import spack.util.module_cmd


def echo(text):
    """Turn some text containing newline characters into a series of
    echo commands that would produce the same output if run in a shell.
    """
    lines = text.split('\n')
    return '\n'.join(['echo "{0}"'.format(line) for line in lines])


@pytest.fixture(scope='module')
def compiler_version_data():
    """Return a dictionary with data on compiler version messages"""
    data_dir = os.path.join(spack.paths.test_path, 'data', 'compilers')
    yaml_file = os.path.join(data_dir, 'version_output.yaml')
    with open(yaml_file) as f:
        data = syaml.load(f)
    return data


@pytest.mark.parametrize('compiler_name', [
    'apple-clang', 'arm', 'cce', 'clang', 'fj',
    'gcc', 'intel', 'nag', 'pgi', 'xlc', 'xlf'
])
@pytest.mark.regression('10191')
def test_version_detection(
        compiler_name, compiler_version_data, mock_executable
):
    # Version output data is stored in data/compilers/version_output.yaml
    for data in compiler_version_data[compiler_name]:
        exe_name, pkg_name = data['name'], data.get('package', compiler_name)
        expected_version, message = data['version'], data['message']
        exe = mock_executable(
            exe_name, echo(message), subdir=(expected_version, 'bin')
        )
        version = spack.repo.get(pkg_name).determine_version(exe)
        assert version == expected_version
