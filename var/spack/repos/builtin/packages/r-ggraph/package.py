# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgraph(RPackage):
    """ggraph: An Implementation of Grammar of Graphics for Graphs and
       Networks"""

    homepage = "https://cloud.r-project.org/package=ggraph"
    url      = "https://cloud.r-project.org/src/contrib/ggraph_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggraph"

    version('1.0.2', sha256='4c24739ecabfc65c290a11980491a20bdaac675392a98dc30ccde76ac4b8f53a')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.2:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-ggforce', type=('build', 'run'))
    depends_on('r-grid', type=('build', 'run'))
    depends_on('r-igraph@1.0.0:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-stats', type=('build', 'run'))
    depends_on('r-viridis', type=('build', 'run'))
