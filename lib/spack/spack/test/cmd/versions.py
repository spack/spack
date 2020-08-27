# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

versions = SpackCommand('versions')


def test_safe_versions():
    """Only test the safe versions of a package."""

    versions('--safe-only', 'zlib')


@pytest.mark.network
def test_remote_versions():
    """Test a package for which remote versions should be available."""

    versions('zlib')


@pytest.mark.network
def test_no_versions():
    """Test a package for which no remote versions are available."""

    versions('converge')


@pytest.mark.network
def test_no_unchecksummed_versions():
    """Test a package for which no unchecksummed versions are available."""

    versions('bzip2')


@pytest.mark.network
def test_versions_no_url():
    """Test a package with versions but without a ``url`` attribute."""

    versions('graphviz')


@pytest.mark.network
def test_no_versions_no_url():
    """Test a package without versions or a ``url`` attribute."""

    versions('opengl')
