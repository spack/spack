##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest

from spack.main import SpackCommand

versions = SpackCommand('versions')


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
