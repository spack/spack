# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import sys

import pytest

from llnl.util.filesystem import mkdirp

import spack
from spack.util.executable import which
from spack.version import ver

git = which("git")
git_required_version = '2.17.0'


def check_git_version():
    """Check if git version is new enough for worktree functionality.
    Return True if requirements are met.

    The latest required functionality is `worktree remove` which was only added
    in 2.17.0.

    Refer:
    https://github.com/git/git/commit/cc73385cf6c5c229458775bc92e7dbbe24d11611
    """
    git_version = spack.fetch_strategy.GitFetchStrategy.version_from_git(git)
    return git_version >= ver(git_required_version)


pytestmark = pytest.mark.skipif(
    not git or not check_git_version(),
    reason="we need git to test if we are in a git repo"
)


@pytest.fixture(scope="function")
def git_tmp_worktree(tmpdir):
    """Create new worktree in a temporary folder and monkeypatch
    spack.paths.prefix to point to it.
    """
    # TODO: This is fragile and should be high priority for
    # follow up fixes. 27021
    # Path length is occasionally too long on Windows
    # the following reduces the path length to acceptable levels
    if sys.platform == 'win32':
        long_pth = str(tmpdir).split(os.path.sep)
        tmp_worktree = os.path.sep.join(long_pth[:-1])
    else:
        tmp_worktree = str(tmpdir)
    worktree_root = os.path.sep.join([tmp_worktree, "wrktree"])

    mkdirp(worktree_root)

    git("worktree", "add", "--detach", worktree_root, "HEAD")

    yield worktree_root

    git("worktree", "remove", "--force", worktree_root)


def test_is_git_repo_in_worktree(git_tmp_worktree):
    """Verify that spack.cmd.spack_is_git_repo() can identify a git repository
    in a worktree.
    """
    assert spack.cmd.is_git_repo(git_tmp_worktree)


def test_spack_is_git_repo_nongit(tmpdir, monkeypatch):
    """Verify that spack.cmd.spack_is_git_repo() correctly returns False if we
    are in a non-git directory.
    """
    assert not spack.cmd.is_git_repo(str(tmpdir))
