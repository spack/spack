# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAda(RPackage):
    """Performs discrete, real, and gentle boost under both exponential
    and logistic loss on a given data set."""

    homepage = "https://cran.r-project.org/web/packages/ada/index.html"
    url      = "https://cran.r-project.org/src/contrib/ada_2.0-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ada"

    version('2.0-5', '25ac0dc2650fba9e19f3d15c7c6721c1')

    depends_on('r-rpart', type=('build', 'run'))
