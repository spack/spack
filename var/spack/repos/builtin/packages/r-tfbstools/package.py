# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTfbstools(RPackage):
    """TFBSTools is a package for the analysis and manipulation of
       transcription factor binding sites.

       It includes matrices conversion between Position Frequency Matirx (PFM),
       Position Weight Matirx (PWM) and Information Content Matrix (ICM). It
       can also scan putative TFBS from sequence/alignment, query JASPAR
       database and provides a wrapper of de novo motif discovery software.
       TFBSTools is a package for the analysis and manipulation of
       transcription factor binding sites. It includes matrices conversion
       between Position Frequency Matirx (PFM), Position Weight Matirx (PWM)
       and Information Content Matrix (ICM). It can also scan putative TFBS
       from sequence/alignment, query JASPAR database and provides a wrapper
       of de novo motif discovery software."""

    homepage = "http://bioconductor.org/packages/TFBSTools/"
    git      = "https://git.bioconductor.org/packages/TFBSTools.git"

    version('1.16.0', commit='565436a5a674d4dea7279e796a20c5bd2034f65a')

    depends_on('r-biobase@2.28:', type=('build', 'run'))
    depends_on('r-biostrings@2.36.4:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.14.0:', type=('build', 'run'))
    depends_on('r-biocparallel@1.2.21:', type=('build', 'run'))
    depends_on('r-bsgenome@1.36.3:', type=('build', 'run'))
    depends_on('r-catools@1.17.1:', type=('build', 'run'))
    depends_on('r-cner@1.4.0:', type=('build', 'run'))
    depends_on('r-dirichletmultinomial@1.10.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.6.1:', type=('build', 'run'))
    depends_on('r-genomicranges@1.20.6:', type=('build', 'run'))
    depends_on('r-gtools@3.5.0:', type=('build', 'run'))
    depends_on('r-iranges@2.2.7:', type=('build', 'run'))
    depends_on('r-dbi@0.6:', type=('build', 'run'))
    depends_on('r-rsqlite@1.0.0:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.28.10:', type=('build', 'run'))
    depends_on('r-seqlogo@1.34.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))
    depends_on('r-tfmpvalue@0.0.5:', type=('build', 'run'))
    depends_on('r-xml@3.98-1.3:', type=('build', 'run'))
    depends_on('r-xvector@0.8.0:', type=('build', 'run'))
    depends_on('r@3.4.3:3.4.9', when='@1.16.0')
