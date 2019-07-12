# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAneufinder(RPackage):
    """Analysis of Copy Number Variation in Single-Cell-Sequencing Data

       AneuFinder implements functions for copy-number detection, breakpoint
       detection, and karyotype and heterogeneity analysis in single-cell whole
       genome sequencing and strand-seq data."""

    homepage = "https://bioconductor.org/packages/AneuFinder"
    git      = "https://git.bioconductor.org/packages/AneuFinder.git"

    version('1.12.0', commit='03b83109376b2a9b6a69d57d4a73d91770de2bbf')
    version('1.10.2', commit='56578ae69abac93dfea6bcac1fc205b14b6ba9dd')
    version('1.8.0', commit='36a729d244add5aafbe21c37a1baaea6a50354d3')
    version('1.6.0', commit='0cfbdd1951fb4df5622e002260cfa86294d65d1d')
    version('1.4.0', commit='e5bdf4d5e4f84ee5680986826ffed636ed853b8e')

    depends_on('r@3.6.0:3.6.9', when='@1.12.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.10.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.8.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.0', type=('build', 'run'))
