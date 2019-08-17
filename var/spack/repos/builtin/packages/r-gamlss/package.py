# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGamlss(RPackage):
    """gamlss: Generalised Additive Models for Location Scale and Shape"""

    homepage = "https://cran.r-project.org/package=gamlss"
    url      = "https://cran.r-project.org/src/contrib/gamlss_5.1-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gamlss/"

    version('5.1-2', sha256='0d404e74768a8f98c6a5e9a48bd2cf4280125831a5dcd8c7f7b57922f57e016b')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-gamlss-data@5.0-0:', type=('build', 'run'))
    depends_on('r-gamlss-dist@4.3.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
