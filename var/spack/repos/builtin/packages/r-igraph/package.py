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
    url      = "https://cloud.r-project.org/src/contrib/igraph_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/igraph"

    version('1.2.4.1', sha256='891acc763b5a4a4a245358a95dee69280f4013c342f14dd6a438e7bb2bf2e480')
    version('1.2.4', sha256='1048eb26ab6b592815bc269c1d91e974c86c9ab827ccb80ae0a40042019592cb')
    version('1.1.2', 'ca1617aea272852d2856c4661ad1c7d8')
    version('1.0.1', 'ea33495e49adf4a331e4ba60ba559065')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pkgconfig@2.0.0:', type=('build', 'run'))
    depends_on('r-irlba', when='@:1.1.9', type=('build', 'run'))
    depends_on('gmp')
    depends_on('libxml2')
    depends_on('glpk', when='@1.2.0:')
