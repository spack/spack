# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNnet(RPackage):
    """Software for feed-forward neural networks with a single hidden layer,
    and for multinomial log-linear models."""

    homepage = "http://www.stats.ox.ac.uk/pub/MASS4/"
    url      = "https://cran.r-project.org/src/contrib/nnet_7.3-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/nnet"

    version('7.3-12', 'dc7c6f0d0de53d8fc72b44554400a74e')
