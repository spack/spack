# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.repo
import spack.paths


# Unlike the repo_path fixture defined in conftest, this has a test-level
# scope rather than a session level scope, since we want to edit the
# given RepoPath
@pytest.fixture()
def repo_for_test():
    return spack.repo.RepoPath(spack.paths.mock_packages_path)


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


def test_repo_getpkg(repo_for_test):
    repo_for_test.get('a')
    repo_for_test.get('builtin.mock.a')


def test_repo_multi_getpkg(repo_for_test, extra_repo):
    repo_for_test.put_first(extra_repo)
    repo_for_test.get('a')
    repo_for_test.get('builtin.mock.a')


def test_repo_multi_getpkgclass(repo_for_test, extra_repo):
    repo_for_test.put_first(extra_repo)
    repo_for_test.get_pkg_class('a')
    repo_for_test.get_pkg_class('builtin.mock.a')


def test_repo_pkg_with_unknown_namespace(repo_for_test):
    with pytest.raises(spack.repo.UnknownNamespaceError):
        repo_for_test.get('unknown.a')


def test_repo_unknown_pkg(repo_for_test):
    with pytest.raises(spack.repo.UnknownPackageError):
        repo_for_test.get('builtin.mock.nonexistentpackage')
