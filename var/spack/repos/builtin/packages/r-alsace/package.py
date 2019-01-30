# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAlsace(RPackage):
    """Alternating Least Squares (or Multivariate Curve Resolution)
    for analytical chemical data, in particular hyphenated data where
    the first direction is a retention time axis, and the second a
    spectral axis. Package builds on the basic als function from the
    ALS package and adds functionality for high-throughput analysis,
    including definition of time windows, clustering of profiles,
    retention time correction, etcetera."""

    homepage = "https://www.bioconductor.org/packages/alsace/"
    git      = "https://git.bioconductor.org/packages/alsace.git"

    version('1.12.0', commit='1364c65bbff05786d05c02799fd44fd57748fae3')

    depends_on('r-als', type=('build', 'run'))
    depends_on('r-ptw', type=('build', 'run'))
