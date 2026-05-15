# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.cmd.list
import spack.paths
import spack.repo
import spack.util.git
from spack.main import SpackCommand
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
        "git@github.com:username/spack-packages.git",
        "https://github.com/username/spack-packages.git",
        "git@github.com:username/spack.git",
        "https://github.com/username/spack.git",
    ],
)
def test_list_url_schemes(mock_util_executable, url):
    """Confirm the command handles supported repository URLs."""
    pkg_name = "hdf5"

    _, _, registered_responses = mock_util_executable
    registered_responses["config"] = url
    registered_responses["rev-parse"] = f"path/to/builtin/packages/{pkg_name}/"

    output = list("--format", "version_json", pkg_name)
    assert f"{registered_responses['rev-parse']}package.py" in output
    assert os.path.basename(url).replace(".git", "") in output


def test_list_format_local_repo(tmp_path: pathlib.Path):
    """Confirm a file path is returned for local repository."""
    pkg_name = "mypkg"
    repo_root = tmp_path / "repos" / "spack_repo" / "builtin"
    repo_root.mkdir(parents=True)
    (repo_root / "repo.yaml").write_text("repo:\n  namespace: builtin\n  api: v2.2\n")
    package_root = repo_root / "packages" / pkg_name
    package_root.mkdir(parents=True)
    (package_root / "package.py").write_text(
        """\
from spack.package import *

class Mypkg(Package):
    pass
"""
    )

    test_repo = spack.repo.from_path(str(repo_root))
    with spack.repo.use_repositories(test_repo):
        # Confirm a path is returned when fail to retrieve the remote origin URL
        output = list("--format", "version_json", pkg_name)
        assert "github.com" not in output
        assert f"packages/{pkg_name}/package.py" in output


def test_list_format_non_github_repo(tmp_path: pathlib.Path, mock_util_executable):
    """Confirm a file path is returned for a non-github repository."""
    pkg_name = "mypkg"
    repo_root = tmp_path / "my" / "project" / "spack_repo" / "builtin"
    repo_root.mkdir(parents=True)
    (repo_root / "repo.yaml").write_text("repo:\n  namespace: builtin\n  api: v2.2\n")
    package_root = repo_root / "packages" / pkg_name
    package_root.mkdir(parents=True)
    package_path = package_root / "package.py"
    package_path.write_text(
        """\
from spack.package import *

class Mypkg(Package):
    pass
"""
    )

    test_repo = spack.repo.from_path(str(repo_root))
    with spack.repo.use_repositories(test_repo):
        # Confirm a path is returned for a non-standard spack repository
        _, _, registered_responses = mock_util_executable
        registered_responses["config"] = "https://gitlab.com/username/my-packages.git"
        registered_responses["rev-parse"] = str(package_root) + os.sep

        output = list("--format", "version_json", pkg_name)
        assert package_path.as_uri() in output


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


def test_list_count():
    output = list("--count")
    assert int(output.strip()) == len(spack.repo.all_package_names())

    output = list("--count", "py-")
    assert int(output.strip()) == len(
        [name for name in spack.repo.all_package_names() if "py-" in name]
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

        # Check that missing git results in the file path
        monkeypatch.setattr(spack.util.git, "git", lambda: None)
        filepath = spack.cmd.list.github_url(pkg)
        assert filepath and filepath.startswith("file://"), (
            "Expected missing 'git' results in a file URI"
        )
