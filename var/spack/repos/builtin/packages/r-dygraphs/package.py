# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDygraphs(RPackage):
    """An R interface to the 'dygraphs' JavaScript charting library (a copy of
    which is included in the package). Provides rich facilities for charting
    time-series data in R, including highly configurable series- and
    axis-display and interactive features like zoom/pan and series/point
    highlighting."""

    homepage = "https://cran.r-project.org/web/packages/dygraphs/index.html"
    url      = "https://cran.r-project.org/src/contrib/dygraphs_0.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dygraphs"

    version('0.9', '7f0ce4312bcd3f0a58b8c03b2772f833')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-xts', type=('build', 'run'))
