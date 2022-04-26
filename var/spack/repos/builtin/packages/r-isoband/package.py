# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIsoband(RPackage):
    """Generate Isolines and Isobands from Regularly Spaced Elevation Grids.

    A fast C++ implementation to generate contour lines (isolines) and contour
    polygons (isobands) from regularly spaced grids containing elevation
    data."""

    cran = "isoband"

    version('0.2.5', sha256='46f53fa066f0966f02cb2bf050190c0d5e950dab2cdf565feb63fc092c886ba5')
    version('0.2.3', sha256='f9d3318fdf6d147dc2e2c7015ea7de42a55fa33d6232b952f982df96066b7ffe')

    depends_on('r-testthat', type=('build', 'run'))
