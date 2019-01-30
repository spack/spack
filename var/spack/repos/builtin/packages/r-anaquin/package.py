# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnaquin(RPackage):
    """The project is intended to support the use of sequins
    (synthetic sequencing spike-in controls) owned and made available
    by the Garvan Institute of Medical Research. The goal is to
    provide a standard open source library for quantitative analysis,
    modelling and visualization of spike-in controls."""

    homepage = "https://www.bioconductor.org/packages/Anaquin/"
    git      = "https://git.bioconductor.org/packages/Anaquin.git"

    version('1.2.0', commit='584d1970cc9dc1d354f9a6d7c1306bd7e8567119')

    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
    depends_on('r-deseq2', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
