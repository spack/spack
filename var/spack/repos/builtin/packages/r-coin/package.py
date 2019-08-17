# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCoin(RPackage):
    """Conditional inference procedures for the general independence problem
    including two-sample, K-sample (non-parametric ANOVA), correlation,
    censored, ordered and multivariate problems."""

    homepage = "https://cran.r-project.org/package=coin"
    url      = "https://cran.r-project.org/src/contrib/coin_1.1-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/coin"

    version('1.1-3', '97d3d21f1e4a5762e36dd718dd2d0661')

    depends_on('r@2.14.0:')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-modeltools@0.2-9:', type=('build', 'run'))
    depends_on('r-mvtnorm@1.0-5:', type=('build', 'run'))
    depends_on('r-multcomp', type=('build', 'run'))
