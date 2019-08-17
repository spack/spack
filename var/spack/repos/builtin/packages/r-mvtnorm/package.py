# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMvtnorm(RPackage):
    """Computes multivariate normal and t probabilities, quantiles, random
    deviates and densities."""

    homepage = "http://mvtnorm.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/mvtnorm_1.0-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mvtnorm"

    version('1.0-6', 'cb69426868fd3e330412b8491901d9d4')
    version('1.0-5', '5894dd3969bbfa26f4862c45f9a48a52')
