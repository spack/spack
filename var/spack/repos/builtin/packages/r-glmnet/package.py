# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlmnet(RPackage):
    """Extremely efficient procedures for fitting the entire lasso or
    elastic-net regularization path for linear regression, logistic and
    multinomial regression models, Poisson regression and the Cox model. Two
    recent additions are the multiple-response Gaussian, and the grouped
    multinomial. The algorithm uses cyclical coordinate descent in a path-wise
    fashion, as described in the paper linked to via the URL below."""

    homepage = "https://cran.rstudio.com/web/packages/glmnet/index.html"
    url      = "https://cran.rstudio.com/src/contrib/glmnet_2.0-13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/glmnet"
    version('2.0-13', '1dd5636388df5c3a29207d0bf1253343')
    version('2.0-5', '049b18caa29529614cd684db3beaec2a')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
