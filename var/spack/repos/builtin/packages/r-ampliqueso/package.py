# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAmpliqueso(RPackage):
    """The package provides tools and reports for the analysis of
    amplicon sequencing panels, such as AmpliSeq."""

    homepage = "https://www.bioconductor.org/packages/ampliQueso/"
    git      = "https://git.bioconductor.org/packages/ampliQueso.git"

    version('1.14.0', commit='9a4c26ec594171279aba8ab7fe59c4a2ea09b06b')

    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
    depends_on('r-samr', type=('build', 'run'))
    depends_on('r-deseq', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-statmod', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rnaseqmap', type=('build', 'run'))
