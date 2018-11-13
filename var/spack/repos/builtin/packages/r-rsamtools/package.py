# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsamtools(RPackage):
    """This package provides an interface to the 'samtools', 'bcftools', and
       'tabix' utilities (see 'LICENCE') for manipulating SAM (Sequence
       Alignment / Map), FASTA, binary variant call (BCF) and compressed
       indexed tab-delimited (tabix) files."""

    homepage = "https://bioconductor.org/packages/Rsamtools/"
    git      = "https://git.bioconductor.org/packages/Rsamtools.git"

    version('1.32.2', commit='2b3254ccdeb24dc6ad95a93c2eb527021631797e')
    version('1.28.0', commit='dfa5b6abef68175586f21add7927174786412472')

    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.32.2', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.2', type=('build', 'run'))
