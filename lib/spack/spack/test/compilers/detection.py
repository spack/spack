# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test detection of compiler version"""
import os.path

import pytest
import os

import llnl.util.filesystem as fs

import spack.paths
import spack.repo
import spack.util.spack_yaml as syaml

from spack.operating_systems.cray_frontend import CrayFrontend
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


@pytest.mark.parametrize('compiler,version', [
    ('gcc', '8.1.0'),
    ('gcc', '1.0.0-foo'),
    ('pgi', '19.1'),
    ('pgi', '19.1a'),
    ('intel', '9.0.0'),
    ('intel', '0.0.0-foobar')
])
def test_cray_frontend_compiler_detection(
        compiler, version, tmpdir, monkeypatch, working_env
):
    """Test that the Cray frontend properly finds compilers form modules"""
    # setup the fake compiler directory
    compiler_dir = tmpdir.join(compiler)
    compiler_exe = compiler_dir.join('cc').ensure()
    fs.set_executable(str(compiler_exe))

    # mock modules
    def _module(cmd, *args):
        module_name = '%s/%s' % (compiler, version)
        module_contents = 'prepend-path PATH %s' % compiler_dir
        if cmd == 'avail':
            return module_name if compiler in args[0] else ''
        if cmd == 'show':
            return module_contents if module_name in args else ''
    monkeypatch.setattr(spack.operating_systems.cray_frontend, 'module',
                        _module)

    # remove PATH variable
    os.environ.pop('PATH', None)

    # get a CrayFrontend object
    cray_fe_os = CrayFrontend()

    paths = cray_fe_os.compiler_search_paths
    assert paths == [str(compiler_dir)]
