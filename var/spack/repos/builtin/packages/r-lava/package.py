# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLava(RPackage):
    """Estimation and simulation of latent variable models."""

    homepage = "https://cran.r-project.org/package=lava"
    url      = "https://cran.r-project.org/src/contrib/lava_1.4.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lava"

    version('1.4.7', '28039248a7039ba9281d172e4dbf9543')

    depends_on('r@3.0:')

    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
