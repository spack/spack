# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRandomforest(RPackage):
    """Classification and regression based on a forest of trees using random
    inputs."""

    homepage = "https://www.stat.berkeley.edu/~breiman/RandomForests/"
    url      = "https://cran.r-project.org/src/contrib/randomForest_4.6-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/randomForest"

    version('4.6-12', '071c03af974198e861f1475c5bab9e7a')
