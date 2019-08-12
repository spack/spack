# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNetworkd3(RPackage):
    """Creates 'D3' 'JavaScript' network, tree, dendrogram, and Sankey graphs
    from 'R'."""

    homepage = "http://cran.r-project.org/package=networkD3"
    url      = "https://cran.r-project.org/src/contrib/networkD3_0.2.12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/networkD3"

    version('0.2.12', '356fe4be59698e6fb052644bd9659d84')

    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
