# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNmf(RPackage):
    """Provides a framework to perform Non-negative Matrix Factorization (NMF).
    The package implements a set of already published algorithms and seeding
    methods, and provides a framework to test, develop and plug new/custom
    algorithms. Most of the built-in algorithms have been optimized in C++, and
    the main interface function provides an easy way of performing parallel
    computations on multicore machines.."""

    homepage = "http://renozao.github.io/NMF"
    url      = "https://cran.r-project.org/src/contrib/NMF_0.20.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/NMF"

    version('0.20.6', '81df07b3bf710a611db5af24730ff3d0')

    depends_on('r-pkgmaker', type=('build', 'run'))
    depends_on('r-registry', type=('build', 'run'))
    depends_on('r-rngtools', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gridbase', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
