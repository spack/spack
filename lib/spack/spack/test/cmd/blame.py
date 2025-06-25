# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
from pathlib import Path

import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack.cmd.blame
import spack.paths
import spack.util.spack_json as sjson
from spack.cmd.blame import ensure_full_history, git_prefix, package_repo_root
from spack.main import SpackCommand, SpackCommandError
from spack.repo import RepoDescriptors
from spack.util.executable import ProcessError

pytestmark = pytest.mark.usefixtures("git")

blame = SpackCommand("blame")


def test_blame_by_modtime(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame("--time", "mpich")
    assert "LAST_COMMIT" in out
    assert "AUTHOR" in out
    assert "EMAIL" in out


def test_blame_by_percent(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame("--percent", "mpich")
    assert "LAST_COMMIT" in out
    assert "AUTHOR" in out
    assert "EMAIL" in out


def test_blame_file():
    """Sanity check the blame command to make sure it works."""
    with working_dir(spack.paths.prefix):
        out = blame(os.path.join("bin", "spack"))
    assert "LAST_COMMIT" in out
    assert "AUTHOR" in out
    assert "EMAIL" in out


def test_blame_file_missing():
    """Ensure attempt to get blame for missing file fails."""
    with pytest.raises(SpackCommandError):
        out = blame(os.path.join("missing", "file.txt"))
        assert "does not exist" in out


def test_blame_directory():
    """Ensure attempt to get blame for path that is a directory fails."""
    with pytest.raises(SpackCommandError):
        out = blame(".")
        assert "not tracked" in out


def test_blame_file_outside_spack_repo(tmp_path):
    """Ensure attempts to get blame outside a package repository are flagged."""
    test_file = tmp_path / "test"
    test_file.write_text("This is a test")
    with pytest.raises(SpackCommandError):
        out = blame(str(test_file))
        assert "not within a spack repo" in out


def test_blame_spack_not_git_clone(monkeypatch):
    """Ensure attempt to get blame when spack not a git clone fails."""
    non_git_dir = os.path.join(spack.paths.prefix, "..")
    monkeypatch.setattr(spack.paths, "prefix", non_git_dir)

    with pytest.raises(SpackCommandError):
        out = blame(".")
        assert "not in a git clone" in out


def test_blame_json(mock_packages):
    """Ensure that we can output json as a blame."""
    with working_dir(spack.paths.prefix):
        out = blame("--json", "mpich")

    # Test loading the json, and top level keys
    loaded = sjson.load(out)
    assert "authors" in out
    assert "totals" in out

    # Authors should be a list
    assert len(loaded["authors"]) > 0

    # Each of authors and totals has these shared keys
    keys = ["last_commit", "lines", "percentage"]
    for key in keys:
        assert key in loaded["totals"]

    # But authors is a list of multiple
    for key in keys + ["author", "email"]:
        assert key in loaded["authors"][0]


@pytest.mark.not_on_windows("git hangs")
def test_blame_by_git(mock_packages, capfd):
    """Sanity check the blame command to make sure it works."""
    with capfd.disabled():
        out = blame("--git", "mpich")
    assert "class Mpich" in out
    assert '    homepage = "http://www.mpich.org"' in out


def test_repo_root_local_descriptor(mock_git_version_info, monkeypatch):
    """Sanity check blame's package repository root using a local repo descriptor."""

    # create a mock descriptor for the mock local repository
    MockLocalDescriptor = collections.namedtuple("MockLocalDescriptor", ["path"])
    repo_path, filename, _ = mock_git_version_info
    git_repo_path = Path(repo_path)
    spack_repo_path = git_repo_path / "spack_repo"
    spack_repo_path.mkdir()

    repo_descriptor = MockLocalDescriptor(spack_repo_path)

    def _from_config(*args, **kwargs):
        return {"mock": repo_descriptor}

    monkeypatch.setattr(RepoDescriptors, "from_config", _from_config)

    # The parent of the git repository is outside the package repo root
    path = (git_repo_path / "..").resolve()
    prefix = package_repo_root((path / "..").resolve())
    assert prefix is None

    # The base repository directory is the git root of the package repo
    prefix = package_repo_root(git_repo_path)
    assert prefix == git_repo_path

    # The file under the base repository directory also has the package git root
    prefix = package_repo_root(git_repo_path / filename)
    assert prefix == git_repo_path


def test_repo_root_remote_descriptor(mock_git_version_info, monkeypatch):
    """Sanity check blame's package repository root using a remote repo descriptor."""

    # create a mock descriptor for the mock local repository
    MockRemoteDescriptor = collections.namedtuple("MockRemoteDescriptor", ["destination"])
    repo_path, filename, _ = mock_git_version_info
    git_repo_path = Path(repo_path)

    repo_descriptor = MockRemoteDescriptor(git_repo_path)

    def _from_config(*args, **kwargs):
        return {"mock": repo_descriptor}

    monkeypatch.setattr(RepoDescriptors, "from_config", _from_config)

    # The parent of the git repository is outside the package repo root
    path = (git_repo_path / "..").resolve()
    prefix = package_repo_root((path / "..").resolve())
    assert prefix is None

    # The base repository directory is the git root of the package repo
    prefix = package_repo_root(git_repo_path)
    assert prefix == git_repo_path


def test_git_prefix_bad(tmp_path):
    """Exercise git_prefix paths with arguments that will not return success."""
    assert git_prefix("no/such/file.txt") is None

    with pytest.raises(SystemExit):
        out = git_prefix(tmp_path)
        assert "not in a git repository" in out


def test_ensure_full_history_shallow_works(mock_git_version_info, monkeypatch):
    """Ensure a git that "supports" '--unshallow' "completes" without incident."""

    def _git(*args, **kwargs):
        if "--help" in args:
            return "--unshallow"
        else:
            return ""

    repo_path, filename, _ = mock_git_version_info
    shallow_dir = os.path.join(repo_path, ".git", "shallow")
    mkdirp(shallow_dir)

    # Need to patch the blame command's
    monkeypatch.setattr(spack.cmd.blame, "git", _git)
    ensure_full_history(repo_path, filename)


def test_ensure_full_history_shallow_fails(mock_git_version_info, monkeypatch, capsys):
    """Ensure a git that supports '--unshallow' but fails generates useful error."""
    error_msg = "Mock git cannot fetch."

    def _git(*args, **kwargs):
        if "--help" in args:
            return "--unshallow"
        else:
            raise ProcessError(error_msg)

    repo_path, filename, _ = mock_git_version_info
    shallow_dir = os.path.join(repo_path, ".git", "shallow")
    mkdirp(shallow_dir)

    # Need to patch the blame command's since 'git' already used by
    # mock_git_versioninfo
    monkeypatch.setattr(spack.cmd.blame, "git", _git)
    with pytest.raises(SystemExit):
        ensure_full_history(repo_path, filename)

    out = capsys.readouterr()
    assert error_msg in out[1]


def test_ensure_full_history_shallow_old_git(mock_git_version_info, monkeypatch, capsys):
    """Ensure a git that doesn't support '--unshallow' fails."""

    def _git(*args, **kwargs):
        return ""

    repo_path, filename, _ = mock_git_version_info
    shallow_dir = os.path.join(repo_path, ".git", "shallow")
    mkdirp(shallow_dir)

    # Need to patch the blame command's since 'git' already used by
    # mock_git_versioninfo
    monkeypatch.setattr(spack.cmd.blame, "git", _git)
    with pytest.raises(SystemExit):
        ensure_full_history(repo_path, filename)

    out = capsys.readouterr()
    assert "Use a newer" in out[1]
