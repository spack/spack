# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRda(RPackage):
    """Shrunken Centroids Regularized Discriminant Analysis for the
    classification purpose in high dimensional data."""

    homepage = "https://cran.r-project.org/web/packages/rda/index.html"
    url      = "https://cran.r-project.org/src/contrib/rda_1.0.2-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rda"

    version('1.0.2-2', sha256='52ee41249b860af81dc692eee38cd4f8f26d3fbe34cb274f4e118de0013b58bc')
    version('1.0.2-1', '78060c5e054a63a2df4ae4002d7247bc')
