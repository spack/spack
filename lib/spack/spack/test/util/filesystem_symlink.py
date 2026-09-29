# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for Windows symlink functionality."""

import ast
import errno
import os
import pathlib
import sys
import tempfile

import pytest

import spack.paths
import spack.util.filesystem as fs


def _can_symlink() -> bool:
    return sys.platform != "win32" or fs._windows_can_symlink()


def test_symlink_file(tmp_path: pathlib.Path):
    """Test the symlink functionality on all operating systems for a file"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmp_path / "link.txt")
        assert os.path.exists(link_file) is False
        fs.symlink(real_file, link_file)
        assert os.path.samefile(link_file, real_file)
        # Without symlink privileges on Windows this is a hard link, which is not a link
        assert fs.islink(link_file) == _can_symlink()


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


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_source_not_exists(tmp_path: pathlib.Path):
    """Test the symlink method for the case where a source path does not exist"""
    with fs.working_dir(str(tmp_path)):
        test_dir = str(tmp_path)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        with pytest.raises(fs.SymlinkError):
            fs._windows_symlink(real_dir, link_dir)


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
        assert os.path.samefile(link_file, real_file)
        assert fs.islink(link_file) == _can_symlink()
        # Check dirs
        assert not os.path.lexists(link_dir)
        fs.symlink("b", "a/c")
        assert os.path.lexists(link_dir)


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
        # Neither path can be told apart from the other, so neither is a link
        assert not fs.islink(link_file)
        assert not fs.islink(real_file)
        assert not os.path.islink(link_file)


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
def test_windows_read_link(tmp_path: pathlib.Path):
    """Makes sure readlink can read the link source for junctions on windows, and that hard links
    are treated as regular files."""
    with fs.working_dir(str(tmp_path)):
        real_dir_1 = "real_dir_1"
        real_dir_2 = "real_dir_2"
        link_dir_1 = "link_dir_1"
        link_dir_2 = "link_dir_2"
        os.mkdir(real_dir_1)
        os.mkdir(real_dir_2)

        # Create a file and a directory
        _, real_file_1 = tempfile.mkstemp(prefix="real_1", suffix=".txt", dir=".")
        _, real_file_2 = tempfile.mkstemp(prefix="real_2", suffix=".txt", dir=".")
        link_file_1 = "link_1.txt"
        link_file_2 = "link_2.txt"

        # Make hard link/junction
        fs._windows_create_hard_link(real_file_1, link_file_1)
        fs._windows_create_hard_link(real_file_2, link_file_2)
        fs._windows_create_junction(real_dir_1, link_dir_1)
        fs._windows_create_junction(real_dir_2, link_dir_2)

        for path in (link_file_1, link_file_2, real_file_1, real_file_2):
            with pytest.raises(OSError):
                fs.readlink(path)
        assert fs.readlink(link_dir_1) == os.path.abspath(real_dir_1)
        assert fs.readlink(link_dir_2) == os.path.abspath(real_dir_2)


@pytest.mark.only_windows("Test is for Windows specific behavior")
@pytest.mark.parametrize("can_symlink", [True, False])
def test_symlink_relative_source_is_relative_to_link(
    tmp_path: pathlib.Path, monkeypatch, can_symlink: bool
):
    """A relative source is resolved against the link's directory, not the working directory,
    whether or not the fallback to hard links and junctions is used."""
    if can_symlink and not fs._windows_can_symlink():
        pytest.skip("Test requires elevated privileges")
    monkeypatch.setattr(fs, "_windows_can_symlink", lambda: can_symlink)
    with fs.working_dir(str(tmp_path)):
        os.makedirs(os.path.join("a", "b"))
        fs.touch("only_in_cwd")
        fs.touch(os.path.join("a", "in_link_dir"))

        # Exists relative to the working directory only, so the link would be broken
        with pytest.raises(fs.SymlinkError):
            fs.symlink("only_in_cwd", os.path.join("a", "link"))
        assert not os.path.lexists(os.path.join("a", "link"))

        fs.symlink("in_link_dir", os.path.join("a", "file_link"))
        assert os.path.samefile(os.path.join("a", "file_link"), os.path.join("a", "in_link_dir"))

        fs.symlink("b", os.path.join("a", "dir_link"))
        assert os.path.samefile(os.path.join("a", "dir_link"), os.path.join("a", "b"))
        assert fs.islink(os.path.join("a", "dir_link"))


def test_already_exists_error_is_file_exists_error(tmp_path: pathlib.Path):
    """Callers written against os.symlink catch FileExistsError or check for EEXIST"""
    target = tmp_path / "target"
    link = tmp_path / "link"
    target.touch()
    fs.symlink(str(target), str(link))
    with pytest.raises(FileExistsError) as e:
        fs.symlink(str(target), str(link))
    assert e.value.errno == errno.EEXIST
    assert issubclass(fs.AlreadyExistsError, FileExistsError)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_read_junction_special_characters(tmp_path: pathlib.Path):
    """Junction names containing regex metacharacters can be read"""
    with fs.working_dir(str(tmp_path)):
        os.mkdir("real")
        fs._windows_create_junction("real", "gcc+c++")
        assert fs.readlink("gcc+c++") == os.path.abspath("real")
        assert fs._windows_read_junction("gcc+c++") == os.path.abspath("real")


#: Files (relative to ``spack.paths.module_path``) allowed to call ``os.symlink`` directly, and
#: how many times. Only the cross-platform wrapper itself should need to. Do not raise these
#: numbers: use ``spack.util.filesystem.symlink``, which falls back to junctions and hard links
#: on Windows when the user cannot create symbolic links.
_OS_SYMLINK_BASELINE = {"util/filesystem.py": 4}

#: Directories (relative to ``spack.paths.module_path``) not checked for ``os.symlink`` usage
_OS_SYMLINK_EXCLUDE = ("test", "vendor")


def _os_symlink_usages(tree: ast.AST) -> int:
    """Count references to ``os.symlink`` (calls or aliases), ``from os import symlink`` and
    ``pathlib.Path.symlink_to`` calls, which are all ``os.symlink`` under the hood."""
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == "symlink" and isinstance(node.value, ast.Name):
                count += node.value.id == "os"
            elif node.attr == "symlink_to":
                count += 1
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            count += sum(alias.name == "symlink" for alias in node.names)
    return count


def test_os_symlink_usage_does_not_increase():
    """Ensure no new direct uses of ``os.symlink`` are added to core Spack"""
    root = pathlib.Path(spack.paths.module_path)
    usages = {}
    for path in root.rglob("*.py"):
        rel_path = path.relative_to(root)
        if rel_path.parts[0] in _OS_SYMLINK_EXCLUDE:
            continue
        count = _os_symlink_usages(ast.parse(path.read_text(encoding="utf-8")))
        if count:
            usages[rel_path.as_posix()] = count

    increased = {
        rel_path: count
        for rel_path, count in usages.items()
        if count > _OS_SYMLINK_BASELINE.get(rel_path, 0)
    }
    assert not increased, (
        "Direct use of os.symlink increased; use spack.util.filesystem.symlink instead, which "
        f"works on Windows without symlink privileges. Offending files: {increased}"
    )
