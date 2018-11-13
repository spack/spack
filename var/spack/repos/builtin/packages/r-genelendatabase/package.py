# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGenelendatabase(RPackage):
    """Length of mRNA transcripts for a number of genomes and gene ID
       formats, largely based on UCSC table browser"""

    homepage = "https://bioconductor.org/packages/release/data/experiment/html/geneLenDataBase.html"
    git      = "https://git.bioconductor.org/packages/geneLenDataBase.git"

    version('1.16.0', commit='c2a8b2359c6c59388853d6f6d15d71dffb17a198')

    depends_on('r@3.5.0:3.5.9', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.3.15:', type=('build', 'run'))
