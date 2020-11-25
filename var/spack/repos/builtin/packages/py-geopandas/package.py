# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://pypi.io/packages/source/g/geopandas/geopandas-0.5.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'geopandas', 'geopandas.io', 'geopandas.tools', 'geopandas.datasets'
    ]

    version('0.5.0', sha256='d075d2ab61a502ab92ec6b72aaf9610a1340ec24ed07264fcbdbe944b9e68954')
    version('0.4.0', sha256='9f5d24d23f33e6d3267a633025e4d9e050b3a1e86d41a96d3ccc5ad95afec3db')
    version('0.3.0', sha256='e63bb32a3e516d8c9bcd149c22335575defdc5896c8bdf15c836608f152a920b')

    variant('plotting', default=False, description='Include dependencies required for plotting')

    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-shapely', type=('build', 'run'))
    depends_on('py-fiona', type=('build', 'run'))
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-descartes', type=('build', 'run'), when='+plotting')
    depends_on('py-matplotlib', type=('build', 'run'), when='+plotting')
