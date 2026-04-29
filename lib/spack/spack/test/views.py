# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.concretize
from spack.directory_layout import DirectoryLayout
from spack.filesystem_view import SimpleFilesystemView, YamlFilesystemView
from spack.installer import PackageInstaller
from spack.spec import Spec
from spack.test.conftest import FsTree


def test_remove_extensions_ordered(install_mockery, mock_fetch, tmp_path: pathlib.Path):
    view_dir = str(tmp_path / "view")
    layout = DirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)
    e2 = spack.concretize.concretize_one("extension2")
    PackageInstaller([e2.package], explicit=True).install()
    view.add_specs(e2)

    e1 = e2["extension1"]
    view.remove_specs(e1, e2)


@pytest.mark.regression("32456")
def test_view_with_spec_not_contributing_files(mock_packages, tmp_path: pathlib.Path):
    view_dir = str(tmp_path / "view")
    os.mkdir(view_dir)

    layout = DirectoryLayout(view_dir)
    view = SimpleFilesystemView(view_dir, layout)

    a = Spec("pkg-a")
    b = Spec("pkg-b")
    a.set_prefix(str(tmp_path / "a"))
    b.set_prefix(str(tmp_path / "b"))
    a._mark_concrete()
    b._mark_concrete()

    # Create directory structure for a and b, and view
    os.makedirs(a.prefix.subdir)
    os.makedirs(b.prefix.subdir)
    os.makedirs(os.path.join(a.prefix, ".spack"))
    os.makedirs(os.path.join(b.prefix, ".spack"))

    # Add files to b's prefix, but not to a's
    with open(b.prefix.file, "w", encoding="utf-8") as f:
        f.write("file 1")

    with open(b.prefix.subdir.file, "w", encoding="utf-8") as f:
        f.write("file 2")

    # In previous versions of Spack we incorrectly called add_files_to_view
    # with b's merge map. It shouldn't be called at all, since a has no
    # files to add to the view.
    def pkg_a_add_files_to_view(view, merge_map, skip_if_exists=True):
        assert False, "There shouldn't be files to add"

    a.package.add_files_to_view = pkg_a_add_files_to_view

    # Create view and see if files are linked.
    view.add_specs(a, b)
    assert os.path.lexists(os.path.join(view_dir, "file"))
    assert os.path.lexists(os.path.join(view_dir, "subdir", "file"))


def test_view_unique_subdir_becomes_dir_symlink(mock_packages, tmp_path: pathlib.Path):
    """With link_dirs=True, if a directory is only contributed to by a single spec, the view
    should create a symlink to that directory instead of linking individual files."""
    view_dir = str(tmp_path / "view")
    os.mkdir(view_dir)

    layout = DirectoryLayout(view_dir)
    view = SimpleFilesystemView(view_dir, layout, link_type="symlink", link_dirs=True)

    a = Spec("pkg-a")
    b = Spec("pkg-b")
    a.set_prefix(str(tmp_path / "a"))
    b.set_prefix(str(tmp_path / "b"))
    a._mark_concrete()
    b._mark_concrete()

    FsTree(
        tmp_path,
        {
            # metadata dirs for both
            "a/.spack": FsTree.dir(),
            "b/.spack": FsTree.dir(),
            # shared dir "lib" with different files in each
            "a/lib/liba.so": FsTree.file(),
            "b/lib/libb.so": FsTree.file(),
            # unique dir "include/a" and "include/b" with nested content
            "a/include/a/a.h": FsTree.file(),
            "b/include/b/b.h": FsTree.file(),
            # unique dir "bin" but at depth 0, so not deep enough to be symlinked
            "a/bin/a": FsTree.file(),
        },
    )

    view.add_specs(a, b)

    # Shared dir "lib" should be a real directory with individual file symlinks
    lib_dir = os.path.join(view_dir, "lib")
    assert os.path.isdir(lib_dir) and not os.path.islink(lib_dir)
    assert os.path.islink(os.path.join(lib_dir, "liba.so"))
    assert os.path.islink(os.path.join(lib_dir, "libb.so"))

    # Unique dir "include/a" should be a directory symlink
    include_link = os.path.join(view_dir, "include", "a")
    assert os.path.islink(include_link)
    assert os.path.isdir(include_link)
    assert os.path.isfile(os.path.join(include_link, "a.h"))

    # Unique dir "include/b" should be a directory symlink pointing to b's include
    include_b_link = os.path.join(view_dir, "include", "b")
    assert os.path.islink(include_b_link)
    assert os.path.isdir(include_b_link)
    assert os.path.isfile(os.path.join(include_b_link, "b.h"))

    # Unique dir "bin/" is too shallow to be symlinked, so should be an actual dir.
    assert os.path.islink(os.path.join(view_dir, "bin")) is False
    assert os.path.isdir(os.path.join(view_dir, "bin"))
    assert os.path.islink(os.path.join(view_dir, "bin", "a"))


def test_view_no_dir_symlinks(mock_packages, tmp_path: pathlib.Path):
    """With link_dirs=False, no directies are symlinked."""
    view_dir = str(tmp_path / "view")
    os.mkdir(view_dir)

    layout = DirectoryLayout(view_dir)
    view = SimpleFilesystemView(view_dir, layout, link_type="symlink", link_dirs=False)

    a = Spec("pkg-a")
    a.set_prefix(str(tmp_path / "a"))
    a._mark_concrete()

    FsTree(tmp_path, {"a/.spack": FsTree.dir(), "a/include/a/a.h": FsTree.file("header")})

    view.add_specs(a)

    # "include/a" should be a real directory, not a symlink
    include_dir = os.path.join(view_dir, "include", "a")
    assert os.path.isdir(include_dir) and not os.path.islink(include_dir)
    # File should be a symlink.
    ah_path = os.path.join(include_dir, "a.h")
    assert os.path.islink(ah_path)
