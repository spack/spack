# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os

import pytest

from llnl.util.filesystem import working_dir

import spack.paths
import spack.util.spack_json as sjson
from spack.cmd.blame import repo_prefix
from spack.main import SpackCommand, SpackCommandError
from spack.repo import RepoDescriptors

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
        with working_dir(spack.paths.prefix):
            out = blame(os.path.join("no", "such", "file.txt"))
            assert "not within a spack repo" in out


def test_blame_file_outside_spack_repo():
    """Trigger the UnknownNamespaceError path by and failure when attempting
    to get blame outside spack."""
    with pytest.raises(SpackCommandError):
        with working_dir(os.path.join(spack.paths.prefix, "..")):
            out = blame("help.txt")
            assert "not within a spack repo" in out


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


def test_repo_prefix_using_repo_descriptor(tmp_path, monkeypatch):
    """Sanity check blame's repo_prefix using a repo descriptor."""
    # set up a mock repository
    paths = [tmp_path / p for p in ["spack_repo", ".git", os.path.join("spack_repo", "builtin")]]
    for p in paths:
        p.mkdir()

    # create a mock descriptor for the mock repository
    MockDescriptor = collections.namedtuple("MockDescriptor", ["path"])
    repo_descriptor = MockDescriptor(str(paths[0]))

    def _from_config(*args, **kwargs):
        return {"mock": repo_descriptor}

    monkeypatch.setattr(RepoDescriptors, "from_config", _from_config)

    # first a case that falls through to not find a match
    prefix = repo_prefix(os.path.realpath(os.path.join(str(tmp_path), "..")))
    assert prefix is None

    # now the case where the non-spack prefix path is returned
    prefix = repo_prefix(str(paths[-1]))
    assert prefix == tmp_path
