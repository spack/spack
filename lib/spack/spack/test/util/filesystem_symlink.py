# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for cross platform symlink functionality."""

import errno
import os
import pathlib
import sys
import tempfile

import pytest

import spack.util.filesystem as fs

if sys.platform == "win32":
    from spack.util import win_links


@pytest.fixture(params=["symlink", "fallback"] if sys.platform == "win32" else ["symlink"])
def link_mode(request, monkeypatch) -> str:
    """Runs a test with symbolic links and, on Windows, with the junction and hard link fallback
    that ``symlink`` uses when the user cannot create symbolic links."""
    if sys.platform == "win32" and request.param == "fallback":
        monkeypatch.setattr(win_links, "can_symlink", lambda: False)
    elif not fs.can_symlink():
        pytest.skip("Test requires symlink privileges")
    return request.param


def check_link(link_mode: str, src: str, dst: str) -> None:
    """Checks that ``dst`` is the link that ``symlink(src, dst)`` creates in the given mode"""
    if link_mode == "symlink":
        assert os.path.islink(dst)
        assert fs.islink(dst)
        assert fs.readlink(dst) == os.path.normpath(src)
    else:
        # A junction or hard link to src, which is relative to the link's directory as for symlinks
        assert not os.path.islink(dst)
        assert os.path.samefile(os.path.join(os.path.dirname(dst), src), dst)


def test_symlink_file(tmp_path: pathlib.Path, link_mode: str):
    """Test the symlink functionality on all operating systems for a file"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        assert os.path.exists(link_file) is False
        fs.symlink(real_file, link_file)
        check_link(link_mode, real_file, link_file)


def test_symlink_dir(tmp_path: pathlib.Path, link_mode: str):
    """Test the symlink functionality on all operating systems for a directory"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        fs.symlink(real_dir, link_dir)
        check_link(link_mode, real_dir, link_dir)


def test_symlink_src_relative_to_link(tmp_path: pathlib.Path, link_mode: str):
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

        file_src = f"b/{os.path.basename(real_file)}"
        fs.symlink(file_src, f"a/{os.path.basename(link_file)}")
        check_link(link_mode, file_src, link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        fs.symlink("b", "a/c")
        check_link(link_mode, "b", link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_relative_source_is_relative_to_link(tmp_path: pathlib.Path, link_mode: str):
    """A relative source is resolved against the link's directory, not the working directory,
    whether or not the fallback to hard links and junctions is used::

        <tmp_path>                  (working directory)
        |-- only_in_cwd
        `-- a
            |-- b/
            |-- in_link_dir
            |-- link      -> only_in_cwd      error: a/only_in_cwd does not exist
            |-- cwd_link  -> ../only_in_cwd
            |-- file_link -> in_link_dir
            `-- dir_link  -> b
    """
    with fs.working_dir(str(tmp_path)):
        os.makedirs(os.path.join("a", "b"))
        fs.touch("only_in_cwd")
        fs.touch(os.path.join("a", "in_link_dir"))

        # only_in_cwd exists relative to our current working directory, but does not exist
        # relative to the symlink's directory, so creating a symlink pointing to this relative
        # path should fail
        with pytest.raises(fs.SymlinkError):
            fs.symlink("only_in_cwd", os.path.join("a", "link"))
        assert not os.path.lexists(os.path.join("a", "link"))

        # The same file, relative to the symlink's directory
        fs.symlink(os.path.join("..", "only_in_cwd"), os.path.join("a", "cwd_link"))
        check_link(link_mode, os.path.join("..", "only_in_cwd"), os.path.join("a", "cwd_link"))

        fs.symlink("in_link_dir", os.path.join("a", "file_link"))
        check_link(link_mode, "in_link_dir", os.path.join("a", "file_link"))

        fs.symlink("b", os.path.join("a", "dir_link"))
        check_link(link_mode, "b", os.path.join("a", "dir_link"))


def test_symlink_to_existing_path_raises_file_exists_error(tmp_path: pathlib.Path, link_mode: str):
    """Check that fs.symlink has the same behavior as os.symlink when the link path already
    exists (including on Windows when the hard link/junction fallback is used): it raises
    FileExistsError with EEXIST, since callers written against os.symlink catch FileExistsError or
    check for EEXIST"""
    target = tmp_path / "target"
    link = tmp_path / "link"
    target.touch()
    fs.symlink(str(target), str(link))
    with pytest.raises(FileExistsError) as e:
        fs.symlink(str(target), str(link))
    assert e.value.errno == errno.EEXIST
