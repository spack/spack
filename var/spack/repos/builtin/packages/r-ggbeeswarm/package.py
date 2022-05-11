# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGgbeeswarm(RPackage):
    """Categorical Scatter (Violin Point) Plots.

    Provides two methods of plotting categorical scatter plots such that the
    arrangement of points within a category reflects the density of data at
    that region, and avoids over-plotting."""

    cran = "ggbeeswarm"

    version('0.6.0', sha256='bbac8552f67ff1945180fbcda83f7f1c47908f27ba4e84921a39c45d6e123333')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-beeswarm', type=('build', 'run'))
    depends_on('r-ggplot2@2.0:', type=('build', 'run'))
    depends_on('r-vipor', type=('build', 'run'))
