# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgbio(RPackage):
    """Visualization tools for genomic data

       The ggbio package extends and specializes the grammar of graphics for
       biological data. The graphics are designed to answer common scientific
       questions, in particular those often asked of high throughput genomics
       data. All core Bioconductor data structures are supported, where
       appropriate. The package supports detailed views of particular genomic
       regions, as well as genome-wide overviews. Supported overviews include
       ideograms and grand linear views. High-level plots include sequence
       fragment length, edge-linked interval to data view, mismatch pileup, and
       several splicing summaries."""

    homepage = "https://bioconductor.org/packages/ggbio"
    git      = "https://git.bioconductor.org/packages/ggbio.git"

    version('1.32.0', commit='04bd12fbe0b1c5c6b721a5f927e1352765f9bf88')
    version('1.30.0', commit='8b05258b089b06a743352e92058edda06c24cfb7')
    version('1.28.5', commit='594521ca556ef7d97cf4882ecfa54d22c2a2faba')
    version('1.26.1', commit='b4f4c898c92aa1082aa7574f1e5c2a0dae943fbc')
    version('1.24.1', commit='ef04c1bca1330f37152bcc21080cbde94849a094')

    depends_on('r@3.6.0:3.6.9', when='@1.32.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.30.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.28.5', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.26.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.24.1', type=('build', 'run'))

    depends_on('r-annotationdbi', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-annotationfilter', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-biobase', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-biostrings', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-biovizbase@1.23.3:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-bsgenome', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-ensembldb@1.99.13:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.1.16:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.17.13:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-genomicranges@1.21.10:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-ggally', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-ggplot2@1.0.0:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-gridextra', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-gtable', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-hmisc', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-iranges', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-organismdbi', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-reshape2', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-rsamtools@1.17.28:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.16:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-scales', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-summarizedexperiment', when='@1.24.1:', type=('build', 'run'))
    depends_on('r-variantannotation@1.11.4:', when='@1.24.1:', type=('build', 'run'))

    depends_on('r-genomicfeatures@1.29.11:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-genomicranges@1.29.14:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-iranges@2.11.16:', when='@1.26.1:', type=('build', 'run'))

    depends_on('r-biovizbase@1.28.2:', when='@1.28.5:', type=('build', 'run'))
    depends_on('r-rlang', when='@1.28.5:', type=('build', 'run'))

    depends_on('r-biovizbase@1.29.2:', when='@1.30.0:', type=('build', 'run'))
