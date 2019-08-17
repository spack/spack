# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAllelicimbalance(RPackage):
    """Provides a framework for allelic specific expression
    investigation using RNA-seq data."""

    homepage = "http://bioconductor.org/packages/AllelicImbalance/"
    git      = "https://git.bioconductor.org/packages/AllelicImbalance.git"

    version('1.14.0', commit='35958534945819baafde0e13d1eb4d05a514142c')

    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-bsgenome', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-gviz', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-seqinr', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
