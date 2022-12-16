# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path

import pytest

from llnl.util.filesystem import mkdirp, touchp, visit_directory_tree, working_dir
from llnl.util.link_tree import DestinationMergeVisitor, LinkTree, SourceMergeVisitor
from llnl.util.symlink import islink

from spack.stage import Stage


@pytest.fixture()
def stage():
    """Creates a stage with the directory structure for the tests."""
    s = Stage("link-tree-test")
    s.create()

    with working_dir(s.path):
        touchp("source/1")
        touchp("source/a/b/2")
        touchp("source/a/b/3")
        touchp("source/c/4")
        touchp("source/c/d/5")
        touchp("source/c/d/6")
        touchp("source/c/d/e/7")

    yield s

    s.destroy()


@pytest.fixture()
def link_tree(stage):
    """Return a properly initialized LinkTree instance."""
    source_path = os.path.join(stage.path, "source")
    return LinkTree(source_path)


def check_file_link(filename, expected_target):
    assert Path(filename).is_file()
    assert islink(filename)
    assert Path.resolve(os.path.realpath(filename)) == os.path.abspath(expected_target)


def check_dir(filename):
    assert Path(filename).is_dir()


def test_merge_to_new_directory(stage, link_tree):
    with working_dir(stage.path):
        link_tree.merge("dest")

        check_file_link("dest/1", "source/1")
        check_file_link("dest/a/b/2", "source/a/b/2")
        check_file_link("dest/a/b/3", "source/a/b/3")
        check_file_link("dest/c/4", "source/c/4")
        check_file_link("dest/c/d/5", "source/c/d/5")
        check_file_link("dest/c/d/6", "source/c/d/6")
        check_file_link("dest/c/d/e/7", "source/c/d/e/7")

        assert os.path.isabs(os.readlink("dest/1"))
        assert os.path.isabs(os.readlink("dest/a/b/2"))
        assert os.path.isabs(os.readlink("dest/a/b/3"))
        assert os.path.isabs(os.readlink("dest/c/4"))
        assert os.path.isabs(os.readlink("dest/c/d/5"))
        assert os.path.isabs(os.readlink("dest/c/d/6"))
        assert os.path.isabs(os.readlink("dest/c/d/e/7"))

        link_tree.unmerge("dest")

        assert not Path("dest").exists()


def test_merge_to_new_directory_relative(stage, link_tree):
    with working_dir(stage.path):
        link_tree.merge("dest", relative=True)

        check_file_link("dest/1", "source/1")
        check_file_link("dest/a/b/2", "source/a/b/2")
        check_file_link("dest/a/b/3", "source/a/b/3")
        check_file_link("dest/c/4", "source/c/4")
        check_file_link("dest/c/d/5", "source/c/d/5")
        check_file_link("dest/c/d/6", "source/c/d/6")
        check_file_link("dest/c/d/e/7", "source/c/d/e/7")

        assert not os.path.isabs(os.readlink("dest/1"))
        assert not os.path.isabs(os.readlink("dest/a/b/2"))
        assert not os.path.isabs(os.readlink("dest/a/b/3"))
        assert not os.path.isabs(os.readlink("dest/c/4"))
        assert not os.path.isabs(os.readlink("dest/c/d/5"))
        assert not os.path.isabs(os.readlink("dest/c/d/6"))
        assert not os.path.isabs(os.readlink("dest/c/d/e/7"))

        link_tree.unmerge("dest")

        assert not Path("dest").exists()


def test_merge_to_existing_directory(stage, link_tree):
    with working_dir(stage.path):

        touchp("dest/x")
        touchp("dest/a/b/y")

        link_tree.merge("dest")

        check_file_link("dest/1", "source/1")
        check_file_link("dest/a/b/2", "source/a/b/2")
        check_file_link("dest/a/b/3", "source/a/b/3")
        check_file_link("dest/c/4", "source/c/4")
        check_file_link("dest/c/d/5", "source/c/d/5")
        check_file_link("dest/c/d/6", "source/c/d/6")
        check_file_link("dest/c/d/e/7", "source/c/d/e/7")

        assert Path("dest/x").is_file()
        assert Path("dest/a/b/y").is_file()

        link_tree.unmerge("dest")

        assert Path("dest/x").is_file()
        assert Path("dest/a/b/y").is_file()

        assert not Path("dest/1").is_file()
        assert not Path("dest/a/b/2").is_file()
        assert not Path("dest/a/b/3").is_file()
        assert not Path("dest/c/4").is_file()
        assert not Path("dest/c/d/5").is_file()
        assert not Path("dest/c/d/6").is_file()
        assert not Path("dest/c/d/e/7").is_file()


def test_merge_with_empty_directories(stage, link_tree):
    with working_dir(stage.path):
        mkdirp("dest/f/g")
        mkdirp("dest/a/b/h")

        link_tree.merge("dest")
        link_tree.unmerge("dest")

        assert not Path("dest/1").exists()
        assert not Path("dest/a/b/2").exists()
        assert not Path("dest/a/b/3").exists()
        assert not Path("dest/c/4").exists()
        assert not Path("dest/c/d/5").exists()
        assert not Path("dest/c/d/6").exists()
        assert not Path("dest/c/d/e/7").exists()

        assert Path("dest/a/b/h").is_dir()
        assert Path("dest/f/g").is_dir()


def test_ignore(stage, link_tree):
    with working_dir(stage.path):
        touchp("source/.spec")
        touchp("dest/.spec")

        link_tree.merge("dest", ignore=lambda x: x == ".spec")
        link_tree.unmerge("dest", ignore=lambda x: x == ".spec")

        assert not Path("dest/1").exists()
        assert not Path("dest/a").exists()
        assert not Path("dest/c").exists()

        assert Path("source/.spec").is_file()
        assert Path("dest/.spec").is_file()


def test_source_merge_visitor_does_not_follow_symlinked_dirs_at_depth(tmpdir):
    """Given an dir structure like this::

        .
        `-- a
            |-- b
            |   |-- c
            |   |   |-- d
            |   |   |   `-- file
            |   |   `-- symlink_d -> d
            |   `-- symlink_c -> c
            `-- symlink_b -> b

    The SoureMergeVisitor will expand symlinked dirs to directories, but only
    to fixed depth, to avoid exponential explosion. In our current defaults,
    symlink_b will be expanded, but symlink_c and symlink_d will not.
    """
    j = os.path.join
    with tmpdir.as_cwd():
        Path(j("a")).mkdir()
        Path(j("a", "b")).mkdir()
        Path(j("a", "b", "c")).mkdir()
        Path(j("a", "b", "c", "d")).mkdir()
        Path(j("a", "symlink_b")).link_to(j("b"))
        Path(j("a", "b", "symlink_c")).link_to(j("c"))
        Path(j("a", "b", "c", "symlink_d")).link_to(j("d"))
        with open(j("a", "b", "c", "d", "file"), "wb"):
            pass

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir), visitor)
    assert [p for p in visitor.files.keys()] == [
        j("a", "b", "c", "d", "file"),
        j("a", "b", "c", "symlink_d"),  # treated as a file, not expanded
        j("a", "b", "symlink_c"),  # treated as a file, not expanded
        j("a", "symlink_b", "c", "d", "file"),  # symlink_b was expanded
        j("a", "symlink_b", "c", "symlink_d"),  # symlink_b was expanded
        j("a", "symlink_b", "symlink_c"),  # symlink_b was expanded
    ]
    assert [p for p in visitor.directories.keys()] == [
        j("a"),
        j("a", "b"),
        j("a", "b", "c"),
        j("a", "b", "c", "d"),
        j("a", "symlink_b"),
        j("a", "symlink_b", "c"),
        j("a", "symlink_b", "c", "d"),
    ]


def test_source_merge_visitor_cant_be_cyclical(tmpdir):
    """Given an dir structure like this::

        .
        |-- a
        |   `-- symlink_b -> ../b
        |   `-- symlink_symlink_b -> symlink_b
        `-- b
            `-- symlink_a -> ../a

    The SoureMergeVisitor will not expand `a/symlink_b`, `a/symlink_symlink_b` and
    `b/symlink_a` to avoid recursion. The general rule is: only expand symlinked dirs
    pointing deeper into the directory structure.
    """
    j = os.path.join
    with tmpdir.as_cwd():
        Path(j("a")).mkdir()
        Path("b"), j("a", "symlink_b")).link_to(j("..")
        Path(j("a", "symlink_b_b")).link_to(j("symlink_b"))
        Path(j("b")).mkdir()
        Path("a"), j("b", "symlink_a")).link_to(j("..")

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir), visitor)
    assert [p for p in visitor.files.keys()] == [
        j("a", "symlink_b"),
        j("a", "symlink_b_b"),
        j("b", "symlink_a"),
    ]
    assert [p for p in visitor.directories.keys()] == [j("a"), j("b")]


def test_destination_merge_visitor_always_errors_on_symlinked_dirs(tmpdir):
    """When merging prefixes into a non-empty destination folder, and
    this destination folder has a symlinked dir where the prefix has a dir,
    we should never merge any files there, but register a fatal error."""
    j = os.path.join

    # Here example_a and example_b are symlinks.
    with tmpdir.mkdir("dst").as_cwd():
        Path("a").mkdir()
        Path("example_a").link_to("a")
        Path("example_b").link_to("a")

    # Here example_a is a directory, and example_b is a (non-expanded) symlinked
    # directory.
    with tmpdir.mkdir("src").as_cwd():
        Path("example_a").mkdir()
        with open(j("example_a", "file"), "wb"):
            pass
        Path("example_b").link_to("..")

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("src")), visitor)
    visit_directory_tree(str(tmpdir.join("dst")), DestinationMergeVisitor(visitor))

    assert visitor.fatal_conflicts
    conflicts = [c.dst for c in visitor.fatal_conflicts]
    assert "example_a" in conflicts
    assert "example_b" in conflicts


def test_destination_merge_visitor_file_dir_clashes(tmpdir):
    """Tests whether non-symlink file-dir and dir-file clashes as registered as fatal
    errors"""
    with tmpdir.mkdir("a").as_cwd():
        Path("example").mkdir()

    with tmpdir.mkdir("b").as_cwd():
        with open("example", "wb"):
            pass

    a_to_b = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("a")), a_to_b)
    visit_directory_tree(str(tmpdir.join("b")), DestinationMergeVisitor(a_to_b))
    assert a_to_b.fatal_conflicts
    assert a_to_b.fatal_conflicts[0].dst == "example"

    b_to_a = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("b")), b_to_a)
    visit_directory_tree(str(tmpdir.join("a")), DestinationMergeVisitor(b_to_a))
    assert b_to_a.fatal_conflicts
    assert b_to_a.fatal_conflicts[0].dst == "example"
