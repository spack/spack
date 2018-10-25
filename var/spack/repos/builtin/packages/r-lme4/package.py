# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLme4(RPackage):
    """Fit linear and generalized linear mixed-effects models. The models and
    their components are represented using S4 classes and methods. The core
    computational algorithms are implemented using the 'Eigen' C++ library for
    numerical linear algebra and 'RcppEigen' "glue"."""

    homepage = "https://github.com/lme4/lme4/"
    url      = "https://cran.r-project.org/src/contrib/lme4_1.1-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lme4"

    version('1.1-12', 'da8aaebb67477ecb5631851c46207804')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-minqa', type=('build', 'run'))
    depends_on('r-nloptr', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
