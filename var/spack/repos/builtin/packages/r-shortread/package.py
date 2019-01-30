# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShortread(RPackage):
    """This package implements sampling, iteration, and input of FASTQ
    files. The package includes functions for filtering and trimming
    reads, and for generating a quality assessment report. Data are
    represented as DNAStringSet-derived objects, and easily manipulated
    for a diversity of purposes. The package also contains legacy support
    for early single-end, ungapped alignment formats."""

    homepage = "https://www.bioconductor.org/packages/ShortRead/"
    git      = "https://git.bioconductor.org/packages/ShortRead.git"

    version('1.34.2', commit='25daac63b301df66a8ef6e98cc2977522c6786cd')

    depends_on('r@3.4.0:3.4.9', when='@1.34.2')
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
