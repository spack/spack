# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import spack
import spack.cmd.debug
import spack.platforms
import spack.repo
import spack.spec
from spack.main import SpackCommand
from spack.test.conftest import _return_none

debug = SpackCommand("debug")


def test_report():
    out = debug("report")
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))

    assert spack.spack_version in out
    assert spack.get_spack_commit() in out
    assert platform.python_version() in out
    assert str(architecture) in out


def test_get_builtin_repo_info_local_repo(mock_git_version_info, monkeypatch):
    """Confirm local git repo descriptor returns expected path."""
    path = mock_git_version_info[0]

    def _from_config(*args, **kwargs):
        return {"builtin": spack.repo.LocalRepoDescriptor("builtin", path)}

    monkeypatch.setattr(spack.repo.RepoDescriptors, "from_config", _from_config)
    assert path in spack.cmd.debug._get_builtin_repo_info()


def test_get_builtin_repo_info_unsupported_type(mock_git_version_info, monkeypatch):
    """Confirm None is return if the 'builtin' repo descriptor's type is unsupported."""

    def _from_config(*args, **kwargs):
        path = mock_git_version_info[0]
        return {"builtin": path}

    monkeypatch.setattr(spack.repo.RepoDescriptors, "from_config", _from_config)
    assert spack.cmd.debug._get_builtin_repo_info() is None


def test_get_builtin_repo_info_no_builtin(monkeypatch):
    """Confirm None is return if there is no 'builtin' repo descriptor."""

    def _from_config(*args, **kwargs):
        return {"local": "/assumes/no/descriptor/needed"}

    monkeypatch.setattr(spack.repo.RepoDescriptors, "from_config", _from_config)
    assert spack.cmd.debug._get_builtin_repo_info() is None


def test_get_builtin_repo_info_bad_destination(mock_git_version_info, monkeypatch):
    """Confirm git failure of a repository returns None."""

    def _from_config(*args, **kwargs):
        path = mock_git_version_info[0]
        return {"builtin": spack.repo.LocalRepoDescriptor("builtin", f"{path}/missing")}

    monkeypatch.setattr(spack.repo.RepoDescriptors, "from_config", _from_config)
    assert spack.cmd.debug._get_builtin_repo_info() is None


def test_get_spack_repo_info_no_commit(monkeypatch):
    """Confirm the version is returned if there is no spack commit."""

    monkeypatch.setattr(spack, "get_spack_commit", _return_none)
    assert spack.cmd.debug._get_spack_repo_info() == spack.spack_version
