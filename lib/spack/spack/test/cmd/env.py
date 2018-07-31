# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
from six import StringIO

import pytest

import spack.modules
import spack.environment as ev
import spack.util.spack_yaml as syaml
from spack.cmd.env import _environment_concretize, _environment_create
from spack.version import Version


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures(
    'mock_env_path', 'config', 'mutable_mock_packages')


def test_add():
    c = ev.Environment('test')
    c.add('mpileaks')
    assert 'mpileaks' in c.user_specs


def test_concretize():
    c = ev.Environment('test')
    c.add('mpileaks')
    c.concretize()
    env_specs = c._get_environment_specs()
    assert any(x.name == 'mpileaks' for x in env_specs)


def test_env_install(install_mockery, mock_fetch):
    c = ev.Environment('test')
    c.add('cmake-client')
    c.concretize()
    c.install()
    env_specs = c._get_environment_specs()
    spec = next(x for x in env_specs if x.name == 'cmake-client')
    assert spec.package.installed


def test_remove_after_concretize():
    c = ev.Environment('test')
    c.add('mpileaks')
    c.concretize()
    c.add('python')
    c.concretize()
    c.remove('mpileaks')
    env_specs = c._get_environment_specs()
    assert not any(x.name == 'mpileaks' for x in env_specs)


def test_reset_compiler():
    c = ev.Environment('test')
    c.add('mpileaks')
    c.concretize()

    first_spec = c.specs_by_hash[c.concretized_order[0]]
    available = set(['gcc', 'clang'])
    available.remove(first_spec.compiler.name)
    new_compiler = next(iter(available))
    c.reset_os_and_compiler(compiler=new_compiler)

    new_spec = c.specs_by_hash[c.concretized_order[0]]
    assert new_spec.compiler != first_spec.compiler


def test_environment_list():
    c = ev.Environment('test')
    c.add('mpileaks')
    c.concretize()
    c.add('python')
    mock_stream = StringIO()
    c.list(mock_stream)
    list_content = mock_stream.getvalue()
    assert 'mpileaks' in list_content
    assert 'python' in list_content
    mpileaks_spec = c.specs_by_hash[c.concretized_order[0]]
    assert mpileaks_spec.format() in list_content


def test_upgrade_dependency():
    c = ev.Environment('test')
    c.add('mpileaks ^callpath@0.9')
    c.concretize()

    c.upgrade_dependency('callpath')
    env_specs = c._get_environment_specs()
    callpath_dependents = list(x for x in env_specs if 'callpath' in x)
    assert callpath_dependents
    for spec in callpath_dependents:
        assert spec['callpath'].version == Version('1.0')


def test_init_config():
    test_config = """\
user_specs:
- mpileaks
packages:
    mpileaks:
        version: [2.2]
"""
    spack.package_prefs.PackagePrefs._packages_config_cache = None
    spack.package_prefs.PackagePrefs._spec_cache = {}

    _environment_create('test', syaml.load(StringIO(test_config)))
    c = ev.read('test')
    ev.prepare_config_scope(c)
    c.concretize()
    assert any(x.satisfies('mpileaks@2.2')
               for x in c._get_environment_specs())


def test_to_dict():
    c = ev.Environment('test')
    c.add('mpileaks')
    c.concretize()
    context_dict = c.to_dict()
    c_copy = ev.Environment.from_dict('test_copy', context_dict)
    assert c.specs_by_hash == c_copy.specs_by_hash


def test_prepare_repo():
    c = ev.Environment('testx')
    c.add('mpileaks')
    _environment_concretize(c)
    repo = None
    try:
        repo = ev.prepare_repository(c)
        package = repo.get(spack.spec.Spec('mpileaks'))
        assert package.namespace.split('.')[-1] == 'testx'
    finally:
        if repo:
            shutil.rmtree(repo.root)
