# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYapsa(RPackage):
    """This package provides functions and routines useful in the analysis of
       somatic signatures (cf. L. Alexandrov et al., Nature 2013). In
       particular, functions to perform a signature analysis with known
       signatures (LCD = linear combination decomposition) and a signature
       analysis on stratified mutational catalogue (SMC = stratify mutational
       catalogue) are provided."""

    homepage = "http://bioconductor.org/packages/YAPSA/"
    git      = "https://git.bioconductor.org/packages/YAPSA.git"

    version('1.2.0', commit='320809b69e470e30a777a383f8341f93064ec24d')

    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-lsei', type=('build', 'run'))
    depends_on('r-somaticsignatures', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-corrplot', type=('build', 'run'))
    depends_on('r-dendextend', type=('build', 'run'))
    depends_on('r-getoptlong', type=('build', 'run'))
    depends_on('r-gtrellis', type=('build', 'run'))
    depends_on('r-pmcmr', type=('build', 'run'))
    depends_on('r-complexheatmap', type=('build', 'run'))
    depends_on('r-keggrest', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
