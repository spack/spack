# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RScales(RPackage):
    """Graphical scales map data to aesthetics, and provide methods for
    automatically determining breaks and labels for axes and legends."""

    homepage = "https://github.com/hadley/scales"
    url      = "https://cran.r-project.org/src/contrib/scales_0.5.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/scales"

    version('0.5.0', '435f6bd826c5cf8df703ffb8a6750fd1')
    version('0.4.1', '3fb2218866a7fe4c1f6e66790876f85a')
    version('0.4.0', '7b5602d9c55595901192248bca25c099')

    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dichromat', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-munsell', type=('build', 'run'))
    depends_on('r-labeling', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-viridislite', type=('build', 'run'))
