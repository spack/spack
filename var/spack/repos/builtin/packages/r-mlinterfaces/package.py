# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMlinterfaces(RPackage):
    """This package provides uniform interfaces to machine learning
    code for data in R and Bioconductor containers."""

    homepage = "https://www.bioconductor.org/packages/MLInterfaces/"
    git      = "https://git.bioconductor.org/packages/MLInterfaces.git"

    version('1.56.0', commit='31fe6fb20d859fcb01d5552f42bca6bab16cc67f')

    depends_on('r@3.4.0:3.4.9', when='@1.56.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-sfsmisc', type=('build', 'run'))
    depends_on('r-rda', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-fpc', type=('build', 'run'))
    depends_on('r-ggvis', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-gbm', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-threejs', type=('build', 'run'))
    depends_on('r-mlbench', type=('build', 'run'))
