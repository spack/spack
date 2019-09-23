# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://cloud.r-project.org/package=glmnet"
    url      = "https://cloud.r-project.org/src/contrib/glmnet_2.0-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/glmnet"

    version('2.0-18', sha256='e8dce9d7b8105f9cc18ba981d420de64a53b09abee219660d3612915d554256b')
    version('2.0-13', '1dd5636388df5c3a29207d0bf1253343')
    version('2.0-5', '049b18caa29529614cd684db3beaec2a')

    depends_on('r-matrix@1.0-6:', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
