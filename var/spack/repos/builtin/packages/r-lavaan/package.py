# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLavaan(RPackage):
    """Latent Variable Analysis.

    Fit a variety of latent variable models, including confirmatory factor
    analysis, structural equation modeling and latent growth curve models."""

    cran = "lavaan"

    version('0.6-10', sha256='4d6944eb6d5743e7a2a2c7b56aec5d5de78585a52789be235839fb9f5f468c37')
    version('0.6-9', sha256='d404c4eb40686534f9c05f24f908cd954041f66d1072caea4a3adfa83a5f108a')
    version('0.6-8', sha256='40e204909100b7338619ae23cd87e0a4058e581c286da2327f36dbb3834b84a2')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-pbivnorm', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
