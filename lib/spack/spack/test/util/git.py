# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
from typing import Optional

import pytest

import spack.util.executable as exe
import spack.util.git
from spack.llnl.util.filesystem import working_dir


def test_git_not_found(monkeypatch):
    def _mock_find_git() -> Optional[str]:
        return None

    monkeypatch.setattr(spack.util.git, "_find_git", _mock_find_git)

    git = spack.util.git.git(required=False)
    assert git is None

    with pytest.raises(exe.CommandNotFoundError):
        spack.util.git.git(required=True)


def test_modified_files(mock_git_package_changes):
    repo, filename, commits = mock_git_package_changes

    with working_dir(repo.packages_path):
        files = spack.util.git.get_modified_files(from_ref="HEAD~1", to_ref="HEAD")
        assert len(files) == 1
        assert files[0] == filename


def test_init_git_repo(git, tmp_path: pathlib.Path):
    repo_url = "https://github.com/spack/spack.git"
    destination = str(tmp_path / "test_git_init")

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo_url)

        assert "No commits yet" in git("status", output=str)


def test_pull_checkout_commit_any_remote(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, commits = mock_git_version_info
    destination = str(tmp_path / "test_git_checkout_commit")

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_commit(commits[0])

        assert commits[0] in git("rev-parse", "HEAD", output=str)


def test_pull_checkout_commit_specific_remote(git, tmp_path: pathlib.Path, mock_git_version_info):
    """Test fetching a specific commit from a specific remote."""
    repo, _, commits = mock_git_version_info
    destination = str(tmp_path / "test_git_checkout_commit_from_remote")

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_commit(commits[0], remote="origin", depth=1)

        assert commits[0] in git("rev-parse", "HEAD", output=str)


def test_pull_checkout_tag(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, _ = mock_git_version_info
    destination = str(tmp_path / "test_git_checkout_tag")

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_tag("v1.1")

        assert "v1.1" in git("describe", "--exact-match", "--tags", output=str)


def test_pull_checkout_branch(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, _ = mock_git_version_info
    destination = str(tmp_path / "test_git_checkout_branch")

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_branch("1.x")

        assert "1.x" in git("rev-parse", "--abbrev-ref", "HEAD", output=str)

        with open("file.txt", "w", encoding="utf-8") as f:
            f.write("hi harmen")

        with pytest.raises(exe.ProcessError):
            spack.util.git.pull_checkout_branch("main")
