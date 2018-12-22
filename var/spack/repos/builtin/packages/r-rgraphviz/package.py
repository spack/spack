# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRgraphviz(RPackage):
    """Interfaces R with the AT and T graphviz library for plotting
    R graph objects from the graph package."""

    homepage = "http://bioconductor.org/packages/Rgraphviz/"
    git      = "https://git.bioconductor.org/packages/Rgraphviz.git"

    version('2.20.0', commit='eface6298150667bb22eac672f1a45e52fbf8c90')

    depends_on('r@3.4.0:3.4.9', when='@2.20.0')
    depends_on('r-graph', type=('build', 'run'))
