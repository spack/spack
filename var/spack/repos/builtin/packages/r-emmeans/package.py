# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REmmeans(RPackage):
    """Estimated Marginal Means, aka Least-Squares Means.

    Obtain estimated marginal means (EMMs) for many linear, generalized linear,
    and mixed models. Compute contrasts or linear functions of EMMs, trends,
    and comparisons of slopes. Plots and other displays.  Least-squares means
    are discussed, and the term "estimated marginal means" is suggested, in
    Searle, Speed, and Milliken (1980) Population marginal means in the linear
    model: An alternative to least squares means, The American Statistician
    34(4), 216-221 <doi:10.1080/00031305.1980.10483031>."""

    cran = "emmeans"

    version('1.7.2', sha256='d3e51c2a4b6c74dd9840efebe241a53072172f269f4324421f28f68db71721bc')
    version('1.7.1-1', sha256='6b01eaad1ea0f96245db8563cc77929a3c3b96cd61c24ce1d452308d6e0250de')
    version('1.7.0', sha256='d4b654896197dfda8354b33257380a66ee06117d6177b1ed7f1e42176525e9c5')
    version('1.6.0', sha256='201bb7b008dde94231ed60bcc6a32749442faaab4baeea99ad28b97c951b3c1e')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-estimability@1.3:', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-xtable@1.8-2:', type=('build', 'run'))

    depends_on('r-plyr', type=('build', 'run'), when='@:1.6')
