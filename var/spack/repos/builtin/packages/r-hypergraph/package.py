# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHypergraph(RPackage):
    """A package that implements some simple capabilities for
    representing and manipulating hypergraphs."""

    homepage = "https://www.bioconductor.org/packages/hypergraph/"
    git      = "https://git.bioconductor.org/packages/hypergraph.git"

    version('1.48.0', commit='a4c19ea0b5f15204f706a7bfdea5363706382820')

    depends_on('r@3.4.0:3.4.9', when='@1.48.0')
    depends_on('r-graph', type=('build', 'run'))
