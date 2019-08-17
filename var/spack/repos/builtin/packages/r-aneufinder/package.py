# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAneufinder(RPackage):
    """This package implements functions for CNV calling, plotting,
    export and analysis from whole-genome single cell sequencing data."""

    homepage = "https://www.bioconductor.org/packages/AneuFinder/"
    git      = "https://git.bioconductor.org/packages/AneuFinder.git"

    version('1.4.0', commit='e5bdf4d5e4f84ee5680986826ffed636ed853b8e')

    depends_on('r@3.4.0:3.4.9', when='@1.4.0')
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-aneufinderdata', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-bamsignals', type=('build', 'run'))
    depends_on('r-dnacopy', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-ggdendro', type=('build', 'run'))
    depends_on('r-reordercluster', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
