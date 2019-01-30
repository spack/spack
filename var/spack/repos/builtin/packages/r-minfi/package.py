# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMinfi(RPackage):
    """Tools to analyze & visualize Illumina Infinium methylation arrays."""

    homepage = "https://bioconductor.org/packages/minfi/"
    git      = "https://git.bioconductor.org/packages/minfi.git"

    version('1.22.1', commit='b2faf84bcbb291e32d470a0e029450093527545b')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-bumphunter', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-beanplot', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nor1mix', type=('build', 'run'))
    depends_on('r-siggenes', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-illuminaio', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-reshape', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-geoquery', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.22.1')
