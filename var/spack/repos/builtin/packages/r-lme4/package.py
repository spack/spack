# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cloud.r-project.org/src/contrib/lme4_1.1-12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lme4"

    version('1.1-20', sha256='44f45f5cd20ec6a50bf96a939b1db44b1a180dbc871a5e3042baf7a107016b2c')
    version('1.1-12', 'da8aaebb67477ecb5631851c46207804')

    depends_on('r@3.2.0:')
    depends_on('r-matrix@1.2-1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nlme@3.1-123:', type=('build', 'run'))
    depends_on('r-minqa@1.1.15:', type=('build', 'run'))
    depends_on('r-nloptr@1.0.4:', type=('build', 'run'))
    depends_on('r-rcpp@0.10.5:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-boot', when='@1.1-21:', type=('build', 'run'))
