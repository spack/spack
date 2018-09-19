##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
