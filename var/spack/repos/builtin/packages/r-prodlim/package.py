# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProdlim(RPackage):
    """Product-Limit Estimation for Censored Event History Analysis. Fast and
    user friendly implementation of nonparametric estimators for censored event
    history (survival) analysis. Kaplan-Meier and Aalen-Johansen method."""

    homepage = "https://cran.r-project.org/package=prodlim"
    url      = "https://cran.r-project.org/src/contrib/prodlim_1.5.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/prodlim"

    version('1.5.9', 'e0843053c9270e41b657a733d6675dc9')

    depends_on('r@2.9.0:')

    depends_on('r-rcpp@0.11.5:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
    depends_on('r-lava', type=('build', 'run'))
