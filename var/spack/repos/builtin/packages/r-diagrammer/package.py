# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDiagrammer(RPackage):
    """Create graph diagrams and flowcharts using R."""

    homepage = "https://github.com/rich-iannone/DiagrammeR"
    url      = "https://cran.r-project.org/src/contrib/DiagrammeR_0.8.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DiagrammeR"

    version('0.8.4', '9ee295c744f5d4ba9a84289ca7bdaf1a')

    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-influencer', type=('build', 'run'))
    depends_on('r-rstudioapi@0.6:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-visnetwork', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
