# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-opendatacube
#
# You can edit this file again by typing:
#
#     spack edit py-opendatacube
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyOpendatacube(PythonPackage):
    """Open Data Cube analyses continental scale Earth Observation data through time."""

    homepage = "https://www.opendatacube.org"
    url      = "https://github.com/opendatacube/datacube-core/archive/datacube-1.7.tar.gz"

    maintainers = ['petebunting']

    version('1.7', '472a25b9c7c3090f854e8a7725aa67eb')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('postgresql', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-cachetools', type=('build', 'run'))
    depends_on('py-affine', type=('build', 'run'))
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('py-dask', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-psycopg2', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-pypeg2', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-rasterio', type=('build', 'run'))
    depends_on('py-sqlalchemy', type=('build', 'run'))
    depends_on('py-toolz', type=('build', 'run'))
    depends_on('py-xarray', type=('build', 'run'))


