# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGenomicalignments(RPackage):
    """Provides efficient containers for storing and manipulating short genomic
    alignments (typically obtained by aligning short reads to a reference
    genome). This includes read counting, computing the coverage, junction
    detection, and working with the nucleotide content of the alignments."""

    homepage = "https://bioconductor.org/packages/GenomicAlignments/"
    git      = "https://git.bioconductor.org/packages/GenomicAlignments.git"

    version('1.16.0', commit='db032a459e5cf05a2a5c2059662a541827112974')
    version('1.14.2', commit='57b0b35d8b36069d4d94af86af051f0129b28eef')
    version('1.12.2', commit='b5d6f19e4a89b6c1c3e9e58e5ea4eb13870874ef')

    depends_on('r-biocgenerics@0.15.3:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.28:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-iranges@2.5.36:', when='@1.12.2', type=('build', 'run'))
    depends_on('r-iranges@2.11.16:', when='@1.14.2', type=('build', 'run'))
    depends_on('r-iranges@2.13.25:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.5:', when='@1.12.2', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.14.2:', type=('build', 'run'))
    depends_on('r-genomicranges@1.27.19:', when='@1.12.2', type=('build', 'run'))
    depends_on('r-genomicranges@1.29.14:', when='@1.14.2', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.19:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.5.3:', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.9.13:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-biostrings@2.37.1:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-rsamtools@1.21.4:', type=('build', 'run'))
    depends_on('r-rsamtools@1.31.2:', when='@1.16.0', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.12.2:1.15.9', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.16.0', type=('build', 'run'))
