# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RScales(RPackage):
    """Graphical scales map data to aesthetics, and provide methods for
    automatically determining breaks and labels for axes and legends."""

    homepage = "https://github.com/hadley/scales"
    url      = "https://cloud.r-project.org/src/contrib/scales_0.5.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/scales"

    version('1.0.0', sha256='0c1f4a14edd336a404da34a3cc71a6a9d0ca2040ba19360c41a79f36e06ca30c')
    version('0.5.0', '435f6bd826c5cf8df703ffb8a6750fd1')
    version('0.4.1', '3fb2218866a7fe4c1f6e66790876f85a')
    version('0.4.0', '7b5602d9c55595901192248bca25c099')

    depends_on('r@2.13:', when='@:0.5.0', type=('build', 'run'))
    depends_on('r@3.1:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dichromat', when='@:0.5.0', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.5.0', type=('build', 'run'))
    depends_on('r-munsell@0.5:', type=('build', 'run'))
    depends_on('r-labeling', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-viridislite', type=('build', 'run'))
