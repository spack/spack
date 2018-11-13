# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSf(RPackage):
    """Support for simple features, a standardized way to encode spatial
       vector data. Binds to GDAL for reading and writing data, to GEOS for
       geometrical operations, and to Proj.4 for projection conversions and
       datum transformations."""

    homepage = "https://github.com/r-spatial/sf/"
    url      = "https://cran.r-project.org/src/contrib/sf_0.5-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sf"

    version('0.5-5', '53ff32d0c9bf2844666c68ce7d75beb2')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-dbi@0.5:', type=('build', 'run'))
    depends_on('r-units@0.4-6:', type=('build', 'run'))
    depends_on('r-classint', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('gdal@2.0.0:')
    depends_on('geos@3.3.0:')
    depends_on('proj@4.8.0:')
