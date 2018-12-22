# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPathview(RPackage):
    """Pathview is a tool set for pathway based data integration and
    visualization. It maps and renders a wide variety of biological data on
    relevant pathway graphs. All users need is to supply their data and
    specify the target pathway. Pathview automatically downloads the pathway
    graph data, parses the data file, maps user data to the pathway, and
    render pathway graph with the mapped data. In addition, Pathview also
    seamlessly integrates with pathway and gene set (enrichment) analysis
    tools for large-scale and fully automated analysis."""

    homepage = "https://www.bioconductor.org/packages/pathview/"
    git      = "https://git.bioconductor.org/packages/pathview.git"

    version('1.16.7', commit='fc560ed15ef7393a73d35e714716cc24dc835339')

    depends_on('r-keggrest', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rgraphviz', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-kegggraph', type=('build', 'run'))
    depends_on('r-org-hs-eg-db', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.7')
