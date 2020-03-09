# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.repo
import spack.paths


@pytest.fixture()
def extra_repo(tmpdir_factory):
    repo_namespace = 'extra_test_repo'
    repo_dir = tmpdir_factory.mktemp(repo_namespace)
    repo_dir.ensure('packages', dir=True)

    with open(str(repo_dir.join('repo.yaml')), 'w') as f:
        f.write("""
repo:
  namespace: extra_test_repo
""")
    return spack.repo.Repo(str(repo_dir))


def test_repo_getpkg(mutable_mock_repo):
    mutable_mock_repo.get('a')
    mutable_mock_repo.get('builtin.mock.a')


def test_repo_multi_getpkg(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo)
    mutable_mock_repo.get('a')
    mutable_mock_repo.get('builtin.mock.a')


def test_repo_multi_getpkgclass(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo)
    mutable_mock_repo.get_pkg_class('a')
    mutable_mock_repo.get_pkg_class('builtin.mock.a')


def test_repo_pkg_with_unknown_namespace(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownNamespaceError):
        mutable_mock_repo.get('unknown.a')


def test_repo_unknown_pkg(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownPackageError):
        mutable_mock_repo.get('builtin.mock.nonexistentpackage')


@pytest.mark.maybeslow
def test_repo_last_mtime():
    latest_mtime = max(os.path.getmtime(p.module.__file__)
                       for p in spack.repo.path.all_packages())
    assert spack.repo.path.last_mtime() == latest_mtime


def test_repo_invisibles(mutable_mock_repo, extra_repo):
    with open(os.path.join(extra_repo.root, 'packages', '.invisible'), 'w'):
        pass
    extra_repo.all_package_names()
