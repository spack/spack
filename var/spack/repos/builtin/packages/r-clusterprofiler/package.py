# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClusterprofiler(RPackage):
    """This package implements methods to analyze and visualize functional
    profiles (GO and KEGG) of gene and gene clusters."""

    homepage = "https://www.bioconductor.org/packages/clusterProfiler/"
    git      = "https://git.bioconductor.org/packages/clusterProfiler.git"

    version('3.4.4', commit='b86b00e8405fe130e439362651a5567736e2d9d7')

    depends_on('r@3.4.0:3.4.9', when='@3.4.4')
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-rvcheck', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-gosemsim', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-dose', type=('build', 'run'))
