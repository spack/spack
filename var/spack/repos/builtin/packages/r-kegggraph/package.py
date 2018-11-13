# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKegggraph(RPackage):
    """KEGGGraph is an interface between KEGG pathway and graph object as
    well as a collection of tools to analyze, dissect and visualize these
    graphs. It parses the regularly updated KGML (KEGG XML) files into graph
    models maintaining all essential pathway attributes. The package offers
    functionalities including parsing, graph operation, visualization and
    etc."""

    homepage = "https://www.bioconductor.org/packages/KEGGgraph/"
    git      = "https://git.bioconductor.org/packages/KEGGgraph.git"

    version('1.38.1', commit='dd31665beb36d5aad8ed09ed56c603633b6b2292')

    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.38.1')
