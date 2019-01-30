# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCluster(RPackage):
    """Methods for Cluster analysis. Much extended the original from Peter
    Rousseeuw, Anja Struyf and Mia Hubert, based on Kaufman and Rousseeuw
    (1990) "Finding Groups in Data"."""

    homepage = "https://cran.r-project.org/web/packages/cluster/index.html"
    url      = "https://cran.rstudio.com/src/contrib/cluster_2.0.7-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cluster"

    version('2.0.7-1', 'a37add21b91d3e4f3883d005331e0d45')
    version('2.0.5', '7330f209ebce960bdee1a6d6679cb85a')
    version('2.0.4', 'bb4deceaafb1c42bb1278d5d0dc11e59')
