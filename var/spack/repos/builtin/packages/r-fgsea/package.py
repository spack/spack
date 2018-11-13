# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFgsea(RPackage):
    """The package implements an algorithm for fast gene set enrichment
    analysis. Using the fast algorithm allows to make more permutations
    and get more fine grained p-values, which allows to use accurate
    stantard approaches to multiple hypothesis correction."""

    homepage = "https://www.bioconductor.org/packages/fgsea/"
    git      = "https://git.bioconductor.org/packages/fgsea.git"

    version('1.2.1', commit='99b04eef664204d0dca4b9f8027cd7eefb006b72')

    depends_on('r@3.4.0:3.4.9', when='@1.2.1')
    depends_on('r-fastmatch', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
