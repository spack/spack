# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIpred(RPackage):
    """Improved predictive models by indirect classification and bagging for
    classification, regression and survival problems as well as resampling
    based estimators of prediction error."""

    homepage = "https://cran.r-project.org/package=ipred"
    url      = "https://cran.r-project.org/src/contrib/ipred_0.9-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ipred"

    version('0.9-5', 'ce8768547a7aa9554ad3650b18ea3cbd')

    depends_on('r@2.10:')

    depends_on('r-rpart@3.1-8:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-prodlim', type=('build', 'run'))
