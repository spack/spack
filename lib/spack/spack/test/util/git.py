# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
from typing import Optional

import pytest

import spack.util.executable as exe
import spack.util.git
from spack.llnl.util.filesystem import working_dir


def _mock_find_git() -> Optional[str]:
    return None


def test_git_not_found(monkeypatch):
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
    destination = tmp_path / "test_git_init"

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo_url)

        assert "No commits yet" in git("status", output=str)


def test_pull_checkout_commit(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, commits = mock_git_version_info
    destination = tmp_path / "test_git_checkout_commit"

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_commit(commits[0])

        assert commits[0] in git("rev-parse", "HEAD", output=str)


def test_pull_checkout_tag(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, _ = mock_git_version_info
    destination = tmp_path / "test_git_checkout_tag"

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_tag("v1.1")

        assert "v1.1" in git("describe", "--exact-match", "--tags", output=str)


def test_pull_checkout_branch(git, tmp_path: pathlib.Path, mock_git_version_info):
    repo, _, _ = mock_git_version_info
    destination = tmp_path / "test_git_checkout_branch"

    with working_dir(destination, create=True):
        spack.util.git.init_git_repo(repo)
        spack.util.git.pull_checkout_branch("1.x")

        assert "1.x" in git("rev-parse", "--abbrev-ref", "HEAD", output=str)

        with open("file.txt", "w", encoding="utf-8") as f:
            f.write("hi harmen")

        with pytest.raises(exe.ProcessError):
            spack.util.git.pull_checkout_branch("main")


def test_not_git_repo(tmp_path: pathlib.Path):
    result = spack.util.git.git_url_root(str(tmp_path))
    assert result is None


def test_git_url_root(tmp_path: pathlib.Path):
    # Ensure both the url and root have values.
    def _git(*args, **kwargs):
        if "config" in args:
            return "https://mock.com/mock.git"

        if "rev-parse" in args:
            return str(tmp_path)

        return None

    result = spack.util.git.git_url_root(str(tmp_path), _git)
    assert result is not None
    assert result[0] is not None and result[1] is not None


def test_git_url_root_missing_git(
    monkeypatch, tmp_path: pathlib.Path, capfd: pytest.CaptureFixture
):
    monkeypatch.setattr(spack.util.git, "_find_git", _mock_find_git)

    result = spack.util.git.git_url_root(str(tmp_path))
    assert result is None

    captured = capfd.readouterr()
    assert "spack requires 'git'" in captured.err
