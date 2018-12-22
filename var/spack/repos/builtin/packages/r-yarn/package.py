# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYarn(RPackage):
    """Expedite large RNA-Seq analyses using a combination of previously
       developed tools. YARN is meant to make it easier for the user in
       performing basic mis-annotation quality control, filtering, and
       condition-aware normalization. YARN leverages many Bioconductor tools
       and statistical techniques to account for the large heterogeneity and
       sparsity found in very large RNA-seq experiments."""

    homepage = "https://bioconductor.org/packages/yarn/"
    git      = "https://git.bioconductor.org/packages/yarn.git"

    version('1.2.0', commit='28af616ef8c27dcadf6568e276dea8465486a697')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-downloader', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-quantro', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
