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
import filecmp
import os
import pytest

import spack.repo
import spack.mirror
import spack.util.executable
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which

pytestmark = pytest.mark.usefixtures('config', 'mutable_mock_packages')

# paths in repos that shouldn't be in the mirror tarballs.
exclude = ['.hg', '.git', '.svn']


repos = {}


def set_up_package(name, repository, url_attr):
    """Set up a mock package to be mirrored.
    Each package needs us to:

    1. Set up a mock repo/archive to fetch from.
    2. Point the package's version args at that repo.
    """
    # Set up packages to point at mock repos.
    spec = Spec(name)
    spec.concretize()
    # Get the package and fix its fetch args to point to a mock repo
    pkg = spack.repo.get(spec)

    repos[name] = repository

    # change the fetch args of the first (only) version.
    assert len(pkg.versions) == 1
    v = next(iter(pkg.versions))

    pkg.versions[v][url_attr] = repository.url


def check_mirror():
    with Stage('spack-mirror-test') as stage:
        mirror_root = os.path.join(stage.path, 'test-mirror')
        # register mirror with spack config
        mirrors = {'spack-mirror-test': 'file://' + mirror_root}
        spack.config.set('mirrors', mirrors)
        spack.mirror.create(mirror_root, repos, no_checksum=True)

        # Stage directory exists
        assert os.path.isdir(mirror_root)

        # check that there are subdirs for each package
        for name in repos:
            subdir = os.path.join(mirror_root, name)
            assert os.path.isdir(subdir)

            files = os.listdir(subdir)
            assert len(files) == 1

            # Now try to fetch each package.
            for name, mock_repo in repos.items():
                spec = Spec(name).concretized()
                pkg = spec.package

                with spack.config.override('config:checksum', False):
                    with pkg.stage:
                        pkg.do_stage(mirror_only=True)

                        # Compare the original repo with the expanded archive
                        original_path = mock_repo.path
                        if 'svn' in name:
                            # have to check out the svn repo to compare.
                            original_path = os.path.join(
                                mock_repo.path, 'checked_out')

                            svn = which('svn', required=True)
                            svn('checkout', mock_repo.url, original_path)

                        dcmp = filecmp.dircmp(
                            original_path, pkg.stage.source_path)

                        # make sure there are no new files in the expanded
                        # tarball
                        assert not dcmp.right_only
                        # and that all original files are present.
                        assert all(l in exclude for l in dcmp.left_only)


def test_url_mirror(mock_archive):
    set_up_package('trivial-install-test-package', mock_archive, 'url')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not which('git'), reason='requires git to be installed')
def test_git_mirror(mock_git_repository):
    set_up_package('git-test', mock_git_repository, 'git')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not which('svn'), reason='requires subversion to be installed')
def test_svn_mirror(mock_svn_repository):
    set_up_package('svn-test', mock_svn_repository, 'svn')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not which('hg'), reason='requires mercurial to be installed')
def test_hg_mirror(mock_hg_repository):
    set_up_package('hg-test', mock_hg_repository, 'hg')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not all([which('svn'), which('hg'), which('git')]),
    reason='requires subversion, git, and mercurial to be installed')
def test_all_mirror(
        mock_git_repository,
        mock_svn_repository,
        mock_hg_repository,
        mock_archive):

    set_up_package('git-test', mock_git_repository, 'git')
    set_up_package('svn-test', mock_svn_repository, 'svn')
    set_up_package('hg-test', mock_hg_repository, 'hg')
    set_up_package('trivial-install-test-package', mock_archive, 'url')
    check_mirror()
    repos.clear()
