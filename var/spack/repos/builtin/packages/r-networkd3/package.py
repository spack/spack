# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNetworkd3(RPackage):
    """Creates 'D3' 'JavaScript' network, tree, dendrogram, and Sankey graphs
    from 'R'."""

    homepage = "https://cloud.r-project.org/package=networkD3"
    url      = "https://cloud.r-project.org/src/contrib/networkD3_0.2.12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/networkD3"

    version('0.4', sha256='33b82585f1eec6233303ec14033a703d0b17def441c7a0a67bf7e6764c9c9d0b')
    version('0.3', sha256='6f9d6b35bb1562883df734bef8fbec166dd365e34c6e656da7be5f8a8d42343c')
    version('0.2.12', '356fe4be59698e6fb052644bd9659d84')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-htmlwidgets@0.3.2:', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
