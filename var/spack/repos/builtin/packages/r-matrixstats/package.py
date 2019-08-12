# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMatrixstats(RPackage):
    """High-performing functions operating on rows and columns of matrices,
       e.g. col / rowMedians(), col / rowRanks(), and col / rowSds(). Functions
       optimized per data type and for subsetted calculations such that both
       memory usage and processing time is minimized. There are also optimized
       vector-based methods, e.g. binMeans(), madDiff() and
       weightedMedian()."""

    homepage = "https://cran.rstudio.com/web/packages/matrixStats/index.html"
    url      = "https://cran.rstudio.com/src/contrib/matrixStats_0.52.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/matrixStats"

    version('0.52.2', '41b987d3ae96ee6895875c413adcba3c')
