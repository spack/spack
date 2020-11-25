# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import pytest
import sys

from llnl.util.filesystem import FileFilter

import spack.paths
from spack.cmd.flake8 import flake8, setup_parser, changed_files
from spack.repo import Repo
from spack.util.executable import which


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the ``flake8`` command"""
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    return parser


@pytest.fixture(scope='module')
def flake8_package():
    """Flake8 only checks files that have been modified.
    This fixture makes a small change to the ``flake8``
    mock package, yields the filename, then undoes the
    change on cleanup.
    """
    repo = Repo(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name('flake8')
    package = FileFilter(filename)

    # Make the change
    package.filter("state = 'unmodified'", "state = 'modified'", string=True)

    yield filename

    # Undo the change
    package.filter("state = 'modified'", "state = 'unmodified'", string=True)


def test_changed_files(parser, flake8_package):
    args = parser.parse_args([])

    # changed_files returns file paths relative to the root
    # directory of Spack. Convert to absolute file paths.
    files = changed_files(args)
    files = [os.path.join(spack.paths.prefix, path) for path in files]

    # There will likely be other files that have changed
    # when these tests are run
    assert flake8_package in files


# As of flake8 3.0.0, Python 2.6 and 3.3 are no longer supported
# http://flake8.pycqa.org/en/latest/release-notes/3.0.0.html
@pytest.mark.skipif(
    sys.version_info[:2] <= (2, 6) or
    (3, 0) <= sys.version_info[:2] <= (3, 3),
    reason='flake8 no longer supports Python 2.6 or 3.3 and older')
@pytest.mark.skipif(not which('flake8'), reason='flake8 is not installed.')
def test_flake8(parser, flake8_package):
    # Only test the flake8_package that we modified
    # Otherwise, the unit tests would fail every time
    # the flake8 tests fail
    args = parser.parse_args([flake8_package])
    flake8(parser, args)
    # Get even more coverage
    args = parser.parse_args(['--output', '--root-relative', flake8_package])
    flake8(parser, args)
