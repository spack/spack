# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRgdal(RPackage):
    """Provides bindings to the 'Geospatial' Data Abstraction Library
    ('GDAL') (>= 1.6.3) and access to projection/transformation operations
    from the 'PROJ.4' library. The 'GDAL' and 'PROJ.4' libraries are
    external to the package, and, when installing the package from source,
    must be correctly installed first. Both 'GDAL' raster and 'OGR' vector
    map data can be imported into R, and 'GDAL' raster data and 'OGR'
    vector data exported. Use is made of classes defined in the 'sp' package.
    Windows and Mac Intel OS X binaries (including 'GDAL', 'PROJ.4' and
    'Expat') are provided on 'CRAN'."""

    homepage = "https://cran.r-project.org/package=rgdal"
    url      = "https://cran.rstudio.com/src/contrib/rgdal_1.3-9.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/rgdal"

    version('1.3-9', sha256='3e44f88d09894be4c0abd8874d00b40a4a5f4542b75250d098ffbb3ba41e2654')
    version('1.2-16', 'de83bf08519a53de68a7632ecb7f2dc9')

    depends_on('r-sp', type=('build', 'run'))
    depends_on('gdal')
    depends_on('proj')
