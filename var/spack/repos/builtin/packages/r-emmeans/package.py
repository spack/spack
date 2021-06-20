# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REmmeans(RPackage):
    """Estimated Marginal Means, aka Least-Squares Means

    Obtain estimated marginal means (EMMs) for many linear, generalized
    linear, and mixed models. Compute contrasts or linear functions of EMMs,
    trends, and comparisons of slopes. Plots and other displays.
    Least-squares means are discussed, and the term "estimated marginal means"
    is suggested, in Searle, Speed, and Milliken (1980) Population marginal
    means in the linear model: An alternative to least squares means, The
    American Statistician 34(4), 216-221 <doi:10.1080/00031305.1980.10483031>.
    """

    homepage = "https://github.com/rvlenth/emmeans"
    cran     = "emmeans"

    version('1.6.0', sha256='201bb7b008dde94231ed60bcc6a32749442faaab4baeea99ad28b97c951b3c1e')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-estimability@1.3:', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-xtable@1.8-2:', type=('build', 'run'))
