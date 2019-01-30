# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMclust(RPackage):
    """mclust: Gaussian Mixture Modelling for Model-Based Clustering,
    Classification, and Density Estimation"""

    homepage = "http://www.stat.washington.edu/mclust"
    url      = "https://cran.r-project.org/src/contrib/mclust_5.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mclust"

    version('5.3', '74aac9fccdfc78373ce733c1a09176ef')

    depends_on('r@3.0.0:')
