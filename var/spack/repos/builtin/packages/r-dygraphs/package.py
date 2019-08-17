# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://cloud.r-project.org/package=dygraphs"
    url      = "https://cloud.r-project.org/src/contrib/dygraphs_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dygraphs"

    version('1.1.1.6', sha256='c3d331f30012e721a048e04639f60ea738cd7e54e4f930ac9849b95f0f005208')
    version('1.1.1.5', sha256='274035988fdd6833121fd5831692355d383acc828d540788dbcecaf88eb2d72d')
    version('0.9', '7f0ce4312bcd3f0a58b8c03b2772f833')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-htmlwidgets@0.6:', type=('build', 'run'))
    depends_on('r-zoo@1.7-10:', type=('build', 'run'))
    depends_on('r-xts@0.9-7:', type=('build', 'run'))
