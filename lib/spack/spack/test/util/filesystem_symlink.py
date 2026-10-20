# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for cross platform symlink functionality."""

import os
import pathlib
import tempfile

import spack.util.filesystem as fs


def test_symlink_file(tmp_path: pathlib.Path):
    """Test the symlink functionality on all operating systems for a file"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        assert os.path.exists(link_file) is False
        fs.symlink(real_file, link_file)
        assert os.path.exists(link_file)
        assert fs.islink(link_file)


def test_symlink_dir(tmp_path: pathlib.Path):
    """Test the symlink functionality on all operating systems for a directory"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        fs.symlink(real_dir, link_dir)
        assert os.path.exists(link_dir)
        assert fs.islink(link_dir)


def test_symlink_src_relative_to_link(tmp_path: pathlib.Path):
    """Test the symlink functionality where the source value exists relative to the link
    but not relative to the cwd"""
    with fs.working_dir(str(tmp_path)):
        subdir_1 = tmp_path / "a"
        subdir_2 = os.path.join(subdir_1, "b")
        link_dir = os.path.join(subdir_1, "c")

        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=subdir_2)
        link_file = os.path.join(subdir_1, "link.txt")

        fs.symlink(f"b/{os.path.basename(real_file)}", f"a/{os.path.basename(link_file)}")
        assert os.path.exists(link_file)
        assert fs.islink(link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        fs.symlink("b", "a/c")
        assert os.path.lexists(link_dir)
