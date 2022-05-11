# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.environment as ev
import spack.repo
from spack.main import SpackCommand
from spack.version import Version

stage = SpackCommand('stage')
env = SpackCommand('env')

pytestmark = pytest.mark.usefixtures('install_mockery', 'mock_packages')


@pytest.mark.skipif(sys.platform == 'win32', reason="not implemented on windows")
def test_stage_spec(monkeypatch):
    """Verify that staging specs works."""

    expected = set(['trivial-install-test-package', 'mpileaks'])

    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package_base.PackageBase, 'do_stage', fake_stage)

    stage('trivial-install-test-package', 'mpileaks')

    assert len(expected) == 0


@pytest.fixture(scope='function')
def check_stage_path(monkeypatch, tmpdir):
    expected_path = os.path.join(str(tmpdir), 'x')

    def fake_stage(pkg, mirror_only=False):
        assert pkg.path == expected_path
        assert os.path.isdir(expected_path), expected_path

    monkeypatch.setattr(spack.package_base.PackageBase, 'do_stage', fake_stage)

    return expected_path


@pytest.mark.skipif(sys.platform == 'win32', reason="PermissionError")
def test_stage_path(check_stage_path):
    """Verify that --path only works with single specs."""
    stage('--path={0}'.format(check_stage_path), 'trivial-install-test-package')


def test_stage_path_errors_multiple_specs(check_stage_path):
    """Verify that --path only works with single specs."""
    with pytest.raises(spack.main.SpackCommandError):
        stage('--path={0}'.format(check_stage_path),
              'trivial-install-test-package',
              'mpileaks')


@pytest.mark.skipif(sys.platform == 'win32', reason="not implemented on windows")
def test_stage_with_env_outside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage concretizes specs not in environment instead of erroring."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == 'trivial-install-test-package'
        assert pkg.path is None

    monkeypatch.setattr(spack.package_base.PackageBase, 'do_stage', fake_stage)

    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()

    with e:
        stage('trivial-install-test-package')


@pytest.mark.skipif(sys.platform == 'win32', reason="not implemented on windows")
def test_stage_with_env_inside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment instead of reconcretizing."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == 'mpileaks'
        assert pkg.version == Version('100.100')

    monkeypatch.setattr(spack.package_base.PackageBase, 'do_stage', fake_stage)

    e = ev.create('test')
    e.add('mpileaks@100.100')
    e.concretize()

    with e:
        stage('mpileaks')


@pytest.mark.skipif(sys.platform == 'win32', reason="not implemented on windows")
def test_stage_full_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment."""

    e = ev.create('test')
    e.add('mpileaks@100.100')
    e.concretize()

    # list all the package names that should be staged
    expected = set()
    for spec in e.specs_by_hash.values():
        for dep in spec.traverse():
            expected.add(dep.name)

    # pop the package name from the list instead of actually staging
    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package_base.PackageBase, 'do_stage', fake_stage)

    with e:
        stage()

    # assert that all were staged
    assert len(expected) == 0
