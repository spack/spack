# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGamlssDist(RPackage):
    """gamlss.dist: Distributions for Generalized Additive Models for
       Location Scale and Shape"""

    homepage = "https://cran.r-project.org/package=gamlss.dist"
    url      = "https://cran.r-project.org/src/contrib/gamlss.dist_5.1-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gamlss.dist/"

    version('5.1-1', sha256='44f999ff74ee516757eb39c8308c48aa850523aad2f38e622268313a13dda0b1')

    depends_on('r@2.15:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
