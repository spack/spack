# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLaplacesdemon(RPackage):
    """Provides a complete environment for Bayesian inference using a variety
       of different samplers (see ?LaplacesDemon for an overview). The README
       describes the history of the package development process."""

    homepage = "https://github.com/LaplacesDemonR/LaplacesDemon"
    url      = "https://cran.r-project.org/src/contrib/LaplacesDemon_16.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/LaplacesDemon"

    version('16.0.1', '1e4dab2dd0e27251734d68b0bfdbe911')
