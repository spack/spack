# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RLme4(RPackage):
    """Linear Mixed-Effects Models using 'Eigen' and S4.

    Fit linear and generalized linear mixed-effects models. The models and
    their components are represented using S4 classes and methods. The core
    computational algorithms are implemented using the 'Eigen' C++ library for
    numerical linear algebra and 'RcppEigen' "glue"."""

    cran = "lme4"

    version('1.1-27.1', sha256='25fa873e39b8192e48c15eec93db8c8bf6f03baf3bd8d5ca9188482ce8442ec5')
    version('1.1-27', sha256='fe0391c76c78188ac1eefb18014d0607212c909b55474d985a919b55efe5a15f')
    version('1.1-26', sha256='364b6d6fb0a574dfed2d75cfdc79411aa53e2c1dd625b70bb1d25d026f9e4253')
    version('1.1-21', sha256='7f5554b69ff8ce9bac21e8842131ea940fb7a7dfa2de03684f236d3e3114b20c')
    version('1.1-20', sha256='44f45f5cd20ec6a50bf96a939b1db44b1a180dbc871a5e3042baf7a107016b2c')
    version('1.1-12', sha256='2976b567a4a2144814ff9db987b0aa55c16122c78ecb51b9e09b87fe66a1c048')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.2.0:', type=('build', 'run'), when='@1.1-16:')
    depends_on('r-matrix@1.2-1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'), when='@1.1-21:')
    depends_on('r-nlme@3.1-123:', type=('build', 'run'))
    depends_on('r-minqa@1.1.15:', type=('build', 'run'))
    depends_on('r-nloptr@1.0.4:', type=('build', 'run'))
    depends_on('r-statmod', type=('build', 'run'), when='@1.1-26')
    depends_on('r-rcpp@0.10.5:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
