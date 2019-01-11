# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIgraph(RPackage):
    """Routines for simple graphs and network analysis. It can handle large
    graphs very well and provides functions for generating random and regular
    graphs, graph visualization, centrality methods and much more."""

    homepage = "http://igraph.org/"
    url      = "https://cran.r-project.org/src/contrib/igraph_1.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/igraph"

    version('1.1.2', 'ca1617aea272852d2856c4661ad1c7d8')
    version('1.0.1', 'ea33495e49adf4a331e4ba60ba559065')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('gmp')
    depends_on('libxml2')
