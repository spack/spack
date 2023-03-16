# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``llnl/util/symlink.py``"""
import os
import shutil
import sys
import tempfile

import pytest

from llnl.util import symlink


@pytest.fixture(scope="session")
def stage(tmpdir_factory):
    """Creates a stage with the parent directory for the tests to run in."""

    test_parent_dir = tmpdir_factory.mktemp("symlink_test")
    assert os.path.exists(test_parent_dir)

    # Run tests
    yield test_parent_dir

    # Clean up test directory
    shutil.rmtree(test_parent_dir)


def test_symlink__file(stage):
    """Test the symlink.symlink functionality on all operating systems for a file"""
    test_dir = tempfile.mkdtemp(dir=stage)
    fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
    try:
        assert os.path.exists(real_file)
        link_file = tempfile.mktemp(prefix="link", suffix=".txt", dir=test_dir)
        assert os.path.exists(link_file) is False
        symlink.symlink(real_path=real_file, link_path=link_file)
        assert os.path.exists(link_file)
        assert symlink.islink(link_file)
    finally:
        os.close(fd)


def test_symlink__dir(stage):
    """Test the symlink.symlink functionality on all operating systems for a directory"""
    test_dir = tempfile.mkdtemp(dir=stage)
    real_dir = os.path.join(test_dir, "real_dir")
    link_dir = os.path.join(test_dir, "link_dir")
    os.mkdir(real_dir)
    assert os.path.exists(real_dir)
    symlink.symlink(real_path=real_dir, link_path=link_dir)
    assert os.path.exists(link_dir)
    assert symlink.islink(link_dir)


def test_symlink__source_not_exists(stage):
    """Test the symlink.symlink method for the case where a source path does not exist"""
    test_dir = tempfile.mkdtemp(dir=stage)
    real_dir = os.path.join(test_dir, "real_dir")
    link_dir = os.path.join(test_dir, "link_dir")
    assert not os.path.exists(real_dir)
    assert not os.path.exists(link_dir)
    try:
        symlink.symlink(real_path=real_dir, link_path=link_dir)
        assert False, "symlink command succeeded when it should have failed."
    except symlink.SymlinkError:
        ...


def test_symlink__link_exists(stage):
    """Test the symlink.symlink method for the case where a link already exists"""
    test_dir = tempfile.mkdtemp(dir=stage)
    real_dir = os.path.join(test_dir, "real_dir")
    link_dir = os.path.join(test_dir, "link_dir")
    os.mkdir(real_dir)
    symlink.symlink(real_dir, link_dir)
    assert os.path.exists(real_dir)
    assert os.path.exists(link_dir)
    try:
        symlink.symlink(real_path=real_dir, link_path=link_dir)
        assert False, "symlink command succeeded when it should have failed."
    except symlink.SymlinkError:
        ...


@pytest.mark.skipif(not symlink._windows_can_symlink(), reason="Test requires elevated permissions")
@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_symlink__win_file(stage):
    """Check that symlink.symlink makes a symlink file when run with elevated permissions"""
    test_dir = tempfile.mkdtemp(dir=stage)
    fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
    try:
        assert os.path.exists(real_file)
        link_file = tempfile.mktemp(prefix="link", suffix=".txt", dir=test_dir)
        assert os.path.exists(link_file) is False
        symlink.symlink(real_path=real_file, link_path=link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert symlink.islink(link_file)
        assert os.path.islink(link_file)
        assert not symlink._windows_is_hardlink(link_file)
        assert not symlink._windows_is_junction(link_file)
    finally:
        os.close(fd)


@pytest.mark.skipif(not symlink._windows_can_symlink(), reason="Test requires elevated permissions")
@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_symlink__win_dir(stage):
    """Check that symlink.symlink makes a symlink dir when run with elevated permissions"""
    test_dir = tempfile.mkdtemp(dir=stage)
    real_dir = os.path.join(test_dir, "real")
    link_dir = os.path.join(test_dir, "link")
    os.mkdir(real_dir)
    assert os.path.exists(real_dir)
    symlink.symlink(real_path=real_dir, link_path=link_dir)
    # Verify that all expected conditions are met
    assert os.path.exists(link_dir)
    assert symlink.islink(link_dir)
    assert os.path.islink(link_dir)
    assert not symlink._windows_is_hardlink(link_dir)
    assert not symlink._windows_is_junction(link_dir)


@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_windows_create_junction(stage):
    """Test the symlink._windows_create_junction method"""
    test_dir = tempfile.mkdtemp(dir=stage)
    junction_real_dir = os.path.join(test_dir, "real_dir")
    junction_link_dir = os.path.join(test_dir, "link_dir")
    os.mkdir(junction_real_dir)
    assert os.path.exists(junction_real_dir)
    assert not os.path.exists(junction_link_dir)
    assert symlink._windows_is_junction(junction_real_dir) is False
    symlink._windows_create_junction(junction_real_dir, junction_link_dir)
    # Verify that all expected conditions are met
    assert os.path.exists(junction_link_dir)
    assert symlink._windows_is_junction(junction_link_dir)
    assert symlink.islink(junction_link_dir)
    assert not os.path.islink(junction_link_dir)


@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_windows_create_hard_link(stage):
    """Test the symlink._windows_create_hard_link method"""
    test_dir = tempfile.mkdtemp(dir=stage)
    fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
    try:
        assert os.path.exists(real_file)
        link_file = tempfile.mktemp(prefix="link", suffix=".txt", dir=test_dir)
        assert os.path.exists(link_file) is False
        symlink._windows_create_hard_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert symlink._windows_is_hardlink(real_file)
        assert symlink._windows_is_hardlink(link_file)
        assert symlink.islink(link_file)
        assert not os.path.islink(link_file)
    finally:
        os.close(fd)


@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_windows_create_link__dir(stage):
    """Test the functionality of the windows_create_link method with a directory
    which should result in making a junction.
    """
    test_dir = tempfile.mkdtemp(dir=stage)
    real_dir = os.path.join(test_dir, "real")
    link_dir = os.path.join(test_dir, "link")
    os.mkdir(real_dir)
    assert os.path.exists(real_dir)
    assert not os.path.exists(link_dir)
    symlink._windows_create_link(real_dir, link_dir)
    # Verify that all expected conditions are met
    assert os.path.exists(real_dir)
    assert os.path.exists(link_dir)
    assert symlink.islink(link_dir)
    assert not symlink._windows_is_hardlink(link_dir)
    assert symlink._windows_is_junction(link_dir)
    assert not os.path.islink(link_dir)


@pytest.mark.skipif(sys.platform != "win32", reason="Test is only for Windows")
def test_windows_create_link__file(stage):
    """Test the functionality of the windows_create_link method with a file
    which should result in the creation of a hard link.
    """
    test_dir = tempfile.mkdtemp(dir=stage)
    fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
    try:
        assert os.path.exists(real_file)
        link_file = tempfile.mktemp(prefix="link", suffix=".txt", dir=test_dir)
        assert os.path.exists(link_file) is False
        symlink._windows_create_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert symlink._windows_is_hardlink(real_file)
        assert symlink._windows_is_hardlink(link_file)
        assert symlink.islink(link_file)
        assert not symlink._windows_is_junction(link_file)
        assert not os.path.islink(link_file)
    finally:
        os.close(fd)
