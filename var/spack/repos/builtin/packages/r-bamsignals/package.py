# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBamsignals(RPackage):
    """This package allows to efficiently obtain count vectors
    from indexed bam files. It counts the number of reads in given
    genomic ranges and it computes reads profiles and coverage
    profiles. It also handles paired-end data."""

    homepage = "https://www.bioconductor.org/packages/bamsignals/"
    git      = "https://git.bioconductor.org/packages/bamsignals.git"

    version('1.8.0', commit='b123b83e8e026c9ec91209d4498aff3e95a5de23')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-rhtslib', type=('build', 'run'))
