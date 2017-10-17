##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import spack

import pytest


def test_repo_getpkg():
    repopath = spack.repository.RepoPath(spack.mock_packages_path)
    pkg_a = repopath.get('a')
    pkg_a = repopath.get('builtin.mock.a')


def test_repo_multi_getpkg(tmpdir_factory):
    repopath = spack.repository.RepoPath(spack.mock_packages_path)
    
    repo_namespace = 'extra_test_repo'
    repo_dir = tmpdir_factory.mktemp(repo_namespace)
    repo_dir.ensure('packages', dir=True)
    
    with open(str(repo_dir.join('repo.yaml')), 'w') as F:
        F.write("""
repo:
  namespace: extra_test_repo
""")
    extra_repo = spack.repository.Repo(str(repo_dir))
    repopath.put_first(extra_repo)
    pkg_a = repopath.get('a')
    pkg_a = repopath.get('builtin.mock.a')


def test_repo_multi_getpkgclass(tmpdir_factory):
    repopath = spack.repository.RepoPath(spack.mock_packages_path)
    
    repo_namespace = 'extra_test_repo'
    repo_dir = tmpdir_factory.mktemp(repo_namespace)
    repo_dir.ensure('packages', dir=True)
    
    with open(str(repo_dir.join('repo.yaml')), 'w') as F:
        F.write("""
repo:
  namespace: extra_test_repo
""")
    extra_repo = spack.repository.Repo(str(repo_dir))
    repopath.put_first(extra_repo)
    pkg_a = repopath.get_pkg_class('a')
    pkg_a = repopath.get_pkg_class('builtin.mock.a')
