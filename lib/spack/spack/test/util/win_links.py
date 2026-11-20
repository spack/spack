# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``util/win_links.py``."""

import os
import pathlib
import sys
import tempfile

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

import spack.util.filesystem as fs
from spack.util import win_links


def test_symlink_source_not_exists(tmp_path: pathlib.Path):
    """Test the symlink method for the case where a source path does not exist"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        with pytest.raises(fs.SymlinkError):
            win_links.symlink(real_dir, link_dir)


def test_symlink_src_not_relative_to_link(tmp_path: pathlib.Path):
    """Test the symlink functionality where the source value does not exist relative to
    the link and not relative to the cwd. NOTE that this symlink api call is EXPECTED to raise
    a fs.SymlinkError exception that we catch."""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        subdir_1 = os.path.join(test_dir, "a")
        subdir_2 = os.path.join(subdir_1, "b")
        link_dir = os.path.join(subdir_1, "c")
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=subdir_2)
        link_file = str(tmp_path / "link.txt")
        # Expected SymlinkError because source path does not exist relative to link path
        with pytest.raises(fs.SymlinkError):
            win_links.symlink(
                f"d/{os.path.basename(real_file)}", f"a/{os.path.basename(link_file)}"
            )
        assert not os.path.exists(link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        with pytest.raises(fs.SymlinkError):
            win_links.symlink("d", "a/c")
        assert not os.path.lexists(link_dir)


def test_symlink_link_already_exists(tmp_path: pathlib.Path):
    """Test the symlink method for the case where a link already exists"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        win_links.symlink(real_dir, link_dir)
        assert os.path.exists(link_dir)
        with pytest.raises(fs.SymlinkError):
            win_links.symlink(real_dir, link_dir)


@pytest.mark.skipif(not win_links.can_symlink(), reason="Test requires elevated privileges")
def test_symlink_win_file(tmp_path: pathlib.Path):
    """Check that symlink makes a symlink file when run with elevated permissions"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        fs.symlink(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert fs.islink(link_file)
        assert os.path.islink(link_file)
        assert not win_links.is_hardlink(link_file)
        assert not win_links.is_junction(link_file)


@pytest.mark.skipif(not win_links.can_symlink(), reason="Test requires elevated privileges")
def test_symlink_win_dir(tmp_path: pathlib.Path):
    """Check that symlink makes a symlink dir when run with elevated permissions"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real")
        link_dir = os.path.join(test_dir, "link")
        os.mkdir(real_dir)
        fs.symlink(real_dir, link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(link_dir)
        assert fs.islink(link_dir)
        assert os.path.islink(link_dir)
        assert not win_links.is_hardlink(link_dir)
        assert not win_links.is_junction(link_dir)


def test_windows_create_junction(tmp_path: pathlib.Path):
    """Test the create_junction method"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        junction_real_dir = os.path.join(test_dir, "real_dir")
        junction_link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(junction_real_dir)
        win_links.create_junction(junction_real_dir, junction_link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(junction_link_dir)
        assert win_links.is_junction(junction_link_dir)
        assert fs.islink(junction_link_dir)
        assert not os.path.islink(junction_link_dir)
        # Junctions are only created from absolute paths
        with pytest.raises(fs.SymlinkError):
            win_links.create_junction("real_dir", os.path.join(test_dir, "relative_link_dir"))


def test_windows_create_hard_link(tmp_path: pathlib.Path):
    """Test the create_hard_link method"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        win_links.create_hard_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert win_links.is_hardlink(real_file)
        assert win_links.is_hardlink(link_file)
        # Neither path can be told apart from the other, so neither is a link, and the link can
        # only be recognized given its expected source
        assert not fs.islink(link_file)
        assert not fs.islink(real_file)
        assert not os.path.islink(link_file)
        with pytest.raises(OSError):
            fs.readlink(link_file)
        assert os.path.samefile(real_file, link_file)


def test_windows_create_symlink_fallback_dir(tmp_path: pathlib.Path):
    """The symlink fallback for a directory is a junction"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real")
        link_dir = os.path.join(test_dir, "link")
        os.mkdir(real_dir)
        win_links.create_symlink_fallback(real_dir, link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(link_dir)
        assert fs.islink(link_dir)
        assert not win_links.is_hardlink(link_dir)
        assert win_links.is_junction(link_dir)
        assert not os.path.islink(link_dir)


def test_windows_create_symlink_fallback_file(tmp_path: pathlib.Path):
    """The symlink fallback for a file is a hard link, which islink does not report as a link"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        win_links.create_symlink_fallback(real_file, link_file)
        # Verify that all expected conditions are met
        assert win_links.is_hardlink(link_file)
        assert not fs.islink(link_file)
        assert not win_links.is_junction(link_file)


def test_windows_read_junction(tmp_path: pathlib.Path):
    """Makes sure readlink can read the link source for junctions on windows"""
    with fs.working_dir(str(tmp_path)):
        os.mkdir("real_dir")
        win_links.create_junction(os.path.abspath("real_dir"), "link_dir")
        assert fs.readlink("link_dir") == os.path.abspath("real_dir")


def test_windows_read_junction_special_characters(tmp_path: pathlib.Path):
    """Junction names containing regex metacharacters can be read"""
    with fs.working_dir(str(tmp_path)):
        os.mkdir("real")
        win_links.create_junction(os.path.abspath("real"), "gcc+c++")
        assert fs.readlink("gcc+c++") == os.path.abspath("real")
        assert win_links.read_junction("gcc+c++") == os.path.abspath("real")
