# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCubature(RPackage):
    """Adaptive multivariate integration over hypercubes"""

    homepage = "https://cran.r-project.org/package=cubature"
    url      = "https://cran.r-project.org/src/contrib/cubature_1.1-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cubature"

    version('1.1-2', '5617e1d82baa803a3814d92461da45c9')
