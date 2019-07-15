# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFgsea(RPackage):
    """Fast Gene Set Enrichment Analysis.

       The package implements an algorithm for fast gene set enrichment
       analysis. Using the fast algorithm allows to make more permutations and
       get more fine grained p-values, which allows to use accurate stantard
       approaches to multiple hypothesis correction."""

    homepage = "https://bioconductor.org/packages/fgsea"
    git      = "https://git.bioconductor.org/packages/fgsea.git"

    version('1.10.0', commit='1d4e3e96651d7bfb0c8920873a63591e6f663112')
    version('1.8.0', commit='bb2898aca9fb23e90770671a83fe23f79bb1841b')
    version('1.6.0', commit='52b801b7c2dfd8238fa8f2b402fddb4fda60271d')
    version('1.4.1', commit='73de5ff364e520ac99507a9ee5a61a0d23d3c44e')
    version('1.2.1', commit='99b04eef664204d0dca4b9f8027cd7eefb006b72')

    depends_on('r@3.6.0:3.6.9', when='@1.10.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.8.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.1', type=('build', 'run'))

    depends_on('r-rcpp', when='@1.2.1:', type=('build', 'run'))

    depends_on('r-bh', when='@1.10.0:', type=('build', 'run'))
