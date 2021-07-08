# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

import pytest

from llnl.util.filesystem import FileFilter

import spack.main
import spack.paths
import spack.repo
from spack.cmd.style import changed_files
from spack.util.executable import which

style = spack.main.SpackCommand("style")


@pytest.fixture(scope="function")
def flake8_package():
    """Style only checks files that have been modified. This fixture makes a small
    change to the ``flake8`` mock package, yields the filename, then undoes the
    change on cleanup.
    """
    repo = spack.repo.Repo(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("flake8")
    tmp = filename + ".tmp"

    try:
        shutil.copy(filename, tmp)
        package = FileFilter(filename)
        package.filter("state = 'unmodified'", "state = 'modified'", string=True)
        yield filename
    finally:
        shutil.move(tmp, filename)


@pytest.fixture
def flake8_package_with_errors(scope="function"):
    """A flake8 package with errors."""
    repo = spack.repo.Repo(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("flake8")
    tmp = filename + ".tmp"

    try:
        shutil.copy(filename, tmp)
        package = FileFilter(filename)
        package.filter("state = 'unmodified'", "state    =    'modified'", string=True)
        yield filename
    finally:
        shutil.move(tmp, filename)


def test_changed_files(flake8_package):
    # changed_files returns file paths relative to the root
    # directory of Spack. Convert to absolute file paths.
    files = [os.path.join(spack.paths.prefix, path) for path in changed_files()]

    # There will likely be other files that have changed
    # when these tests are run
    assert flake8_package in files


def test_changed_files_all_files(flake8_package):
    # it's hard to guarantee "all files", so do some sanity checks.
    files = set([
        os.path.join(spack.paths.prefix, path)
        for path in changed_files(all_files=True)
    ])

    # spack has a lot of files -- check that we're in the right ballpark
    assert len(files) > 6000

    # a builtin package
    zlib = spack.repo.path.get_pkg_class("zlib")
    assert zlib.module.__file__ in files

    # a core spack file
    assert os.path.join(spack.paths.module_path, "spec.py") in files

    # a mock package
    assert flake8_package in files

    # this test
    assert __file__ in files

    # ensure externals are excluded
    assert not any(f.startswith(spack.paths.external_path) for f in files)


# As of flake8 3.0.0, Python 2.6 and 3.3 are no longer supported
# http://flake8.pycqa.org/en/latest/release-notes/3.0.0.html
skip_old_python = pytest.mark.skipif(
    sys.version_info[:2] <= (2, 6) or (3, 0) <= sys.version_info[:2] <= (3, 3),
    reason="flake8 no longer supports Python 2.6 or 3.3 and older",
)


@skip_old_python
@pytest.mark.skipif(not which("flake8"), reason="flake8 is not installed.")
def test_style(flake8_package, tmpdir):
    root_relative = os.path.relpath(flake8_package, spack.paths.prefix)

    # use a working directory to test cwd-relative paths, as tests run in
    # the spack prefix by default
    with tmpdir.as_cwd():
        relative = os.path.relpath(flake8_package)

        # no args
        output = style()
        assert relative in output
        assert "spack style checks were clean" in output

        # one specific arg
        output = style(flake8_package)
        assert relative in output
        assert "spack style checks were clean" in output

        # specific file that isn't changed
        output = style(__file__)
        assert relative not in output
        assert __file__ in output
        assert "spack style checks were clean" in output

    # root-relative paths
    output = style("--root-relative", flake8_package)
    assert root_relative in output
    assert "spack style checks were clean" in output


@skip_old_python
@pytest.mark.skipif(not which("flake8"), reason="flake8 is not installed.")
def test_style_with_errors(flake8_package_with_errors):
    root_relative = os.path.relpath(flake8_package_with_errors, spack.paths.prefix)
    output = style("--root-relative", flake8_package_with_errors, fail_on_error=False)
    assert root_relative in output
    assert style.returncode == 1
    assert "spack style found errors" in output


@skip_old_python
@pytest.mark.skipif(not which("flake8"), reason="flake8 is not installed.")
@pytest.mark.skipif(not which("black"), reason="black is not installed.")
def test_style_with_black(flake8_package_with_errors):
    output = style("--black", flake8_package_with_errors, fail_on_error=False)
    assert "black found errors" in output
    assert style.returncode == 1
    assert "spack style found errors" in output
