# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RBlavaan(RPackage):
    """Bayesian Latent Variable Analysis.

Fit a variety of Bayesian latent variable models, including confirmatory factor
analysis, structural equation models, and latent growth curve models.
References: Merkle & Rosseel (2018) <doi:10.18637/jss.v085.i04>; Merkle et al.
(2021) <doi:10.18637/jss.v100.i06>."""

    cran = "blavaan"

    version('0.4-1', sha256='afb077d72f84ef0b6f45ef2ccb8335358042943c32a3472a9ca239ebca1c4aa4')
    version('0.3-18', sha256='373960a22fc741c765e2ad2e0d99c1d4b2162f5f2a230ef314778ef8f433e865')
    version('0.3-15', sha256='f73ead024bc3b65bdb0c5e5cd5458845158914eb579c07be2fd697a3573ebe6f')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-lavaan@0.6-5:', type=('build', 'run'))
    depends_on('r-lavaan@0.6-7:', type=('build', 'run'), when='@0.3-18:')
    depends_on('r-lavaan@0.6-10:', type=('build', 'run'), when='@0.4-1:')
    depends_on('r-rcpp@0.12.15:', type=('build', 'run'))
    depends_on('r-mcmcpack', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-nonnest2@0.5-5:', type=('build', 'run'))
    depends_on('r-loo@2.0:', type=('build', 'run'))
    depends_on('r-rstan@2.19.2:', type=('build', 'run'))
    depends_on('r-rstan@2.21.2:', type=('build', 'run'), when='@0.3-18:')
    depends_on('r-rstantools@1.5.0:', type=('build', 'run'))
    depends_on('r-rcppparallel@5.0.1:', type=('build', 'run'))
    depends_on('r-bayesplot', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-future-apply', type=('build', 'run'))
    depends_on('r-tmvnsim', type=('build', 'run'), when='@0.3-18:')
    depends_on('r-stanheaders@2.18.1:', type=('build', 'run'))
    depends_on('r-bh@1.69.0:', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.4.0:', type=('build', 'run'))
    depends_on('gmake', type='build')
