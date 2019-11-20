# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPhyloseq(RPackage):
    """phyloseq provides a set of classes and tools to facilitate the import,
    storage, analysis, and graphical display of microbiome census data."""

    homepage = "https://www.bioconductor.org/packages/phyloseq/"
    git      = "https://git.bioconductor.org/packages/phyloseq.git"

    version('1.20.0', commit='107d1d5e3437a6e33982c06a548d3cc91df2a7e0')

    depends_on('r@3.4.0:3.4.9', when='@1.20.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-biomformat', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
