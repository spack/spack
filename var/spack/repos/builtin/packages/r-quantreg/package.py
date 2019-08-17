# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQuantreg(RPackage):
    """Estimation and inference methods for models of conditional quantiles:
        Linear and nonlinear parametric and non-parametric (total variation
        penalized) models for conditional quantiles of a univariate response
        and several methods for handling censored survival data. Portfolio
        selection methods based on expected shortfall risk are also
        included."""

    homepage = "https://cran.r-project.org/package=quantreg"
    url      = "https://cran.r-project.org/src/contrib/quantreg_5.29.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/quantreg"

    version('5.29', '643ca728200d13f8c2e62365204e9907')
    version('5.26', '1d89ed932fb4d67ae2d5da0eb8c2989f')

    depends_on('r-sparsem', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-matrixmodels', type=('build', 'run'))
