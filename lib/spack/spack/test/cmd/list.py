# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.cmd.list
import spack.paths
import spack.repo
from spack.main import SpackCommand
from spack.repo import RepoPath
from spack.test.conftest import RepoBuilder

pytestmark = [pytest.mark.usefixtures("mock_packages")]

list = SpackCommand("list")


def test_list():
    output = list()
    assert "bzip2" in output
    assert "hdf5" in output


def test_list_cli_output_format(mock_tty_stdout):
    assert (
        list("mpileaks")
        == """\
mpileaks
==> 1 packages
"""
    )


def test_list_filter():
    output = list("py-*")
    assert "py-extension1" in output
    assert "py-extension2" in output
    assert "py-extension3" in output
    assert "python" not in output
    assert "mpich" not in output

    output = list("py")
    assert "py-extension1" in output
    assert "py-extension2" in output
    assert "py-extension3" in output
    assert "python" in output
    assert "mpich" not in output


def test_list_search_description():
    output = list("--search-description", "one build dependency")
    assert "depb" in output


def test_list_format_name_only():
    output = list("--format", "name_only")
    assert "zmpi" in output
    assert "hdf5" in output


def test_list_format_version_json():
    output = list("--format", "version_json")
    assert '{"name": "zmpi",' in output
    assert '{"name": "dyninst",' in output
    assert "packages/zmpi/package.py" in output

    import json

    json.loads(output)


def test_list_format_html():
    output = list("--format", "html")
    assert '<div class="section" id="zmpi">' in output
    assert "<h1>zmpi" in output

    assert '<div class="section" id="hdf5">' in output
    assert "<h1>hdf5" in output
    assert "packages/hdf5/package.py" in output


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/spack/spack-packages.git",
        "https://github.com/spack/spack-packages",
        "git@github.com:spack/spack-packages.git",
        "ssh://git@github.com/spack/spack-packages.git",
        "https://user:token@github.com/spack/spack-packages.git",
    ],
)
def test_list_url_schemes(mock_git_packages_repo, url):
    """Confirm the official spack-packages repo is recognized in any url scheme."""
    repo = mock_git_packages_repo(url)
    with spack.repo.use_repositories(repo):
        output = list("--format", "version_json", "hdf5")

    assert (
        "https://github.com/spack/spack-packages/blob/develop/"
        "spack_repo/builtin_mock/packages/hdf5/package.py" in output
    )
    # a credentialed url must never leak the credentials into the emitted url
    assert "token" not in output


def test_list_format_local_repo():
    """Confirm a file path is returned for a path-configured (no remote_info) repository."""
    output = list("--format", "version_json", "hdf5")
    assert "github.com" not in output
    assert "file://" in output
    assert "packages/hdf5/package.py" in output


def test_list_format_non_github_repo(mock_git_packages_repo):
    """Confirm a file path is returned for a non-github (e.g. gitlab) repository."""
    repo = mock_git_packages_repo("https://gitlab.com/username/my-packages.git")
    with spack.repo.use_repositories(repo):
        output = list("--format", "version_json", "hdf5")
        assert "github.com" not in output
        assert "file://" in output


def test_list_update(tmp_path: pathlib.Path):
    update_file = tmp_path / "output"

    # not yet created when list is run
    list("--update", str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read()

    # created but older than any package
    with update_file.open("w") as f:
        f.write("empty\n")
    os.utime(str(update_file), (0, 0))  # Set mtime to 0
    list("--update", str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() != "empty\n"

    # newer than any packages
    with update_file.open("w") as f:
        f.write("empty\n")
    list("--update", str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() == "empty\n"


def test_list_tags():
    output = list("--tag", "tag1")
    assert "mpich" in output
    assert "mpich2" in output

    output = list("--tag", "tag2")
    assert "mpich\n" in output
    assert "mpich2" not in output

    output = list("--tag", "tag3")
    assert "mpich\n" not in output
    assert "mpich2" in output


def test_list_count(mock_packages: RepoPath):
    output = list("--count")
    assert int(output.strip()) == len(mock_packages.all_package_names())

    output = list("--count", "py-")
    assert int(output.strip()) == len(
        [name for name in mock_packages.all_package_names() if "py-" in name]
    )


def test_list_repos():
    with spack.repo.use_repositories(
        os.path.join(spack.paths.test_repos_path, "spack_repo", "builtin_mock"),
        os.path.join(spack.paths.test_repos_path, "spack_repo", "builder_test"),
    ):
        total_pkgs = len(list().strip().split())
        mock_pkgs = len(list("-r", "builtin_mock").strip().split())
        builder_pkgs = len(list("-r", "builder_test").strip().split())
        both_repos = len(list("-r", "builtin_mock", "-r", "builder_test").strip().split())

        assert total_pkgs > mock_pkgs > builder_pkgs
        assert both_repos == total_pkgs


@pytest.mark.usefixtures("config")
def test_list_github_url_fails(repo_builder: RepoBuilder, monkeypatch):
    with spack.repo.use_repositories(repo_builder.root):
        repo_builder.add_package("pkg-a")
        repo = spack.repo.PATH.repos[0]
        pkg = repo.get_pkg_class("pkg-a")

        old_path = repo.python_path
        try:
            # Check that a repository with no python path has no URL
            monkeypatch.setattr(repo, "python_path", None)
            assert spack.cmd.list.github_url(pkg) is None, (
                "Expected no python path means unable to determine the repo URL"
            )

            # Check that a repository path that doesn't exist has no URL
            monkeypatch.setattr(repo, "python_path", "/repo/root/does/not/exists")
            assert spack.cmd.list.github_url(pkg) is None, (
                "Expected bad repo path means unable to determine the repo URL"
            )
        finally:
            monkeypatch.setattr(repo, "python_path", old_path)

        # A repository without a configured git url (remote_info is None) yields a file URI
        assert repo.remote_info is None
        filepath = spack.cmd.list.github_url(pkg)
        assert filepath and filepath.startswith("file://"), (
            "Expected a path-configured repo results in a file URI"
        )
