# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRaster(RPackage):
    """Reading, writing, manipulating, analyzing and modeling of gridded
    spatial data. The package implements basic and high-level functions.
    Processing of very large files is supported."""

    homepage = "http://cran.r-project.org/package=raster"
    url      = "https://cran.r-project.org/src/contrib/raster_2.5-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/raster"

    version('2.5-8', '2a7db931c74d50516e82d04687c0a577')

    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
