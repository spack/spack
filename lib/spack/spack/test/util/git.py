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


@pytest.mark.parametrize(
    "input,answer",
    (
        ["git version 1.7.1", (1, 7, 1)],
        ["git version 2.34.1.windows.2", (2, 34, 1)],
        ["git version 2.50.1 (Apple Git-155)", (2, 50, 1)],
        ["git version 1.2.3.4.150.abcd10", (1, 2, 3, 4, 150)],
    ),
)
def test_extract_git_version(mock_util_executable, input, answer):
    _, _, registered_responses = mock_util_executable
    registered_responses["--version"] = input
    git = spack.util.git.GitExecutable()
    assert git.version == answer


def test_mock_git_exe(mock_util_executable):
    log, should_fail, _ = mock_util_executable
    should_fail.append("clone")
    git = spack.util.git.GitExecutable()
    with pytest.raises(exe.ProcessError):
        git("clone")
    assert git.returncode == 1
    git("status")
    assert git.returncode == 0
    assert "clone" in "\n".join(log)
    assert "status" in "\n".join(log)


@pytest.mark.parametrize("git_version", ("1.5.0", "1.3.0"))
def test_git_exe_conditional_option(mock_util_executable, git_version):
    log, _, registered_responses = mock_util_executable
    min_version = (1, 4, 1)
    registered_responses["git --version"] = git_version
    git = spack.util.git.GitExecutable("git")
    mock_opt = spack.util.git.VersionConditionalOption("--maybe", min_version=min_version)
    args = mock_opt(git.version)
    if git.version >= min_version:
        assert "--maybe" in args
    else:
        assert not args


@pytest.mark.parametrize(
    "git_version,ommitted_opts",
    (("2.18.0", ["--filter=blob:none"]), ("1.8.0", ["--filter=blob:none", "--depth"])),
)
def test_git_init_fetch_ommissions(mock_util_executable, git_version, ommitted_opts):
    log, _, registered_responses = mock_util_executable
    registered_responses["git --version"] = git_version
    git = spack.util.git.GitExecutable("git")
    url = "https://foo.git"
    ref = "v1.2.3"
    spack.util.git.git_init_fetch(url, ref, git_exe=git)
    for opt in ommitted_opts:
        assert all(opt not in call for call in log)
