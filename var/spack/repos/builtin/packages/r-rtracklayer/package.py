# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRtracklayer(RPackage):
    """Extensible framework for interacting with multiple genome browsers
       (currently UCSC built-in) and manipulating annotation tracks in various
       formats (currently GFF, BED, bedGraph, BED15, WIG, BigWig and 2bit
       built-in). The user may export/import tracks to/from the supported
       browsers, as well as query and modify the browser state, such as the
       current viewport."""

    homepage = "http://bioconductor.org/packages/rtracklayer/"
    git      = "https://git.bioconductor.org/packages/rtracklayer.git"

    version('1.40.5', commit='4e5b06daccd0bca1ddcd93052deca896ade58fd6')
    version('1.36.6', commit='8c0ac7230f94e0c5a981acbb178c8de70e968131')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.13:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.2:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-rsamtools@1.31.2:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-genomicalignments@1.15.6:', when='@1.40.5', type=('build', 'run'))
    depends_on('r-genomicranges@1.21.20:', when='@1.36.3', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', when='@1.40.5', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.36.6', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.40.5', type=('build', 'run'))
