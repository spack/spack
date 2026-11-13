# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for Windows symlink functionality."""

import errno
import os
import pathlib
import sys
import tempfile

import pytest

import spack.util.filesystem as fs


@pytest.fixture(params=["symlink", "fallback"] if sys.platform == "win32" else ["symlink"])
def link_mode(request, monkeypatch) -> str:
    """Runs a test with symbolic links and, on Windows, with the junction and hard link fallback
    that ``symlink`` uses when the user cannot create symbolic links."""
    if request.param == "fallback":
        monkeypatch.setattr(fs, "_windows_can_symlink", lambda: False)
    elif sys.platform == "win32" and not fs._windows_can_symlink():
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


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_source_not_exists(tmp_path: pathlib.Path):
    """Test the symlink method for the case where a source path does not exist"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        with pytest.raises(fs.SymlinkError):
            fs._windows_symlink(real_dir, link_dir)


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
            fs._windows_symlink(
                f"d/{os.path.basename(real_file)}", f"a/{os.path.basename(link_file)}"
            )
        assert not os.path.exists(link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        with pytest.raises(fs.SymlinkError):
            fs._windows_symlink("d", "a/c")
        assert not os.path.lexists(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_link_already_exists(tmp_path: pathlib.Path):
    """Test the symlink method for the case where a link already exists"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        fs._windows_symlink(real_dir, link_dir)
        assert os.path.exists(link_dir)
        with pytest.raises(fs.SymlinkError):
            fs._windows_symlink(real_dir, link_dir)


@pytest.mark.skipif(not fs._windows_can_symlink(), reason="Test requires elevated privileges")
@pytest.mark.only_windows("Test is for Windows specific behavior")
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
        assert not fs._windows_is_hardlink(link_file)
        assert not fs._windows_is_junction(link_file)


@pytest.mark.skipif(not fs._windows_can_symlink(), reason="Test requires elevated privileges")
@pytest.mark.only_windows("Test is for Windows specific behavior")
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
        assert not fs._windows_is_hardlink(link_dir)
        assert not fs._windows_is_junction(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_junction(tmp_path: pathlib.Path):
    """Test the _windows_create_junction method"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        junction_real_dir = os.path.join(test_dir, "real_dir")
        junction_link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(junction_real_dir)
        fs._windows_create_junction(junction_real_dir, junction_link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(junction_link_dir)
        assert fs._windows_is_junction(junction_link_dir)
        assert fs.islink(junction_link_dir)
        assert not os.path.islink(junction_link_dir)
        # Junctions are only created from absolute paths
        with pytest.raises(fs.SymlinkError):
            fs._windows_create_junction("real_dir", os.path.join(test_dir, "relative_link_dir"))


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_hard_link(tmp_path: pathlib.Path):
    """Test the _windows_create_hard_link method"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        fs._windows_create_hard_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert fs._windows_is_hardlink(real_file)
        assert fs._windows_is_hardlink(link_file)
        # Neither path can be told apart from the other, so neither is a link, and the link can
        # only be recognized given its expected source
        assert not fs.islink(link_file)
        assert not fs.islink(real_file)
        assert not os.path.islink(link_file)
        with pytest.raises(OSError):
            fs.readlink(link_file)
        assert os.path.samefile(real_file, link_file)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_link_dir(tmp_path: pathlib.Path):
    """Test the functionality of the windows_create_link method with a directory
    which should result in making a junction.
    """
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real")
        link_dir = os.path.join(test_dir, "link")
        os.mkdir(real_dir)
        fs._windows_create_link(real_dir, link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(link_dir)
        assert fs.islink(link_dir)
        assert not fs._windows_is_hardlink(link_dir)
        assert fs._windows_is_junction(link_dir)
        assert not os.path.islink(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_link_file(tmp_path: pathlib.Path):
    """Test the functionality of the windows_create_link method with a file
    which should result in the creation of a hard link. It also tests the
    functionality of the symlink islink infrastructure.
    """
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        fs._windows_create_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert fs._windows_is_hardlink(link_file)
        assert not fs.islink(link_file)
        assert not fs._windows_is_junction(link_file)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_read_junction(tmp_path: pathlib.Path):
    """Makes sure readlink can read the link source for junctions on windows"""
    with fs.working_dir(str(tmp_path)):
        os.mkdir("real_dir")
        fs._windows_create_junction(os.path.abspath("real_dir"), "link_dir")
        assert fs.readlink("link_dir") == os.path.abspath("real_dir")


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
    """Like os.symlink, symlink raises FileExistsError with EEXIST when the link path exists, since
    callers written against os.symlink catch FileExistsError or check for EEXIST"""
    target = tmp_path / "target"
    link = tmp_path / "link"
    target.touch()
    fs.symlink(str(target), str(link))
    with pytest.raises(FileExistsError) as e:
        fs.symlink(str(target), str(link))
    assert e.value.errno == errno.EEXIST


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_read_junction_special_characters(tmp_path: pathlib.Path):
    """Junction names containing regex metacharacters can be read"""
    with fs.working_dir(str(tmp_path)):
        os.mkdir("real")
        fs._windows_create_junction(os.path.abspath("real"), "gcc+c++")
        assert fs.readlink("gcc+c++") == os.path.abspath("real")
        assert fs._windows_read_junction("gcc+c++") == os.path.abspath("real")
