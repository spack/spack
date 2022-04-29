# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RScatterpie(RPackage):
    """Scatter Pie Plot.

    Creates scatterpie plots, especially useful for plotting pies on a map."""

    cran = "scatterpie"

    version('0.1.7', sha256='3f7807519cfe135066ca79c8d8a09b59da9aa6d8aaee5e9aff40cca3d0bebade')
    version('0.1.5', sha256='e13237b7effc302acafc1c9b520b4904e55875f4a3b804f653eed2940ca08840')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggforce', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-ggfun', type=('build', 'run'), when='@0.1.7:')
    depends_on('r-tidyr', type=('build', 'run'))

    depends_on('r-rvcheck', type=('build', 'run'), when='@:0.1.5')
