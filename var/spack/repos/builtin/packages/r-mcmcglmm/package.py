# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMcmcglmm(RPackage):
    """MCMC Generalised Linear Mixed Models."""

    homepage = "https://cran.r-project.org/web/packages/MCMCglmm/index.html"
    url      = "https://cran.r-project.org/src/contrib/MCMCglmm_2.25.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/MCMCglmm"

    version('2.25', '260527ef6fecdd87f762fd07406d674a')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-corpcor', type=('build', 'run'))
    depends_on('r-tensora', type=('build', 'run'))
    depends_on('r-cubature', type=('build', 'run'))
