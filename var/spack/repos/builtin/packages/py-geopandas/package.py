# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGeopandas(PythonPackage):
    """GeoPandas is an open source project to make working with geospatial
       data in python easier. GeoPandas extends the datatypes used by pandas
       to allow spatial operations on geometric types. Geometric operations are
       performed by shapely. Geopandas further depends on fiona for file access
       and descartes and matplotlib for plotting."""

    homepage = "http://geopandas.org/"
    url      = "https://github.com/geopandas/geopandas/releases/download/v0.4.0/geopandas-0.4.0.tar.gz"

    version('0.4.0', 'aaad4e27c000d9fa558730d84a9be468')
    version('0.3.0', 'a4211e7a5e113002aec6823ba1368e75')

    variant('plotting', default=False, description='Include dependencies required for plotting')

    depends_on('py-setuptools', type='build')
    depends_on('py-descartes', type=('build', 'run'), when='+plotting')
    depends_on('py-matplotlib', type=('build', 'run'), when='+plotting')
    depends_on('py-fiona', type=('build', 'run'))
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-shapely', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
