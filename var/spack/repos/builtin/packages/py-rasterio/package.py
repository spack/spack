# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRasterio(PythonPackage):
    """Rasterio reads and writes geospatial raster data.
    Geographic information systems use GeoTIFF and other formats to
    organize and store gridded, or raster, datasets. Rasterio reads
    and writes these formats and provides a Python API based on N-D
    arrays."""

    homepage = "https://github.com/mapbox/rasterio"
    url      = "https://github.com/mapbox/rasterio/archive/1.0a12.zip"

    version('1.0a12', 'e078ca02b3513b65a9be5bb3f528b4da')

    variant('aws', default=False,
        description='Enable testing with Amazon Web Services')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    # Only use py-enum34 with Python2
    # depends_on('py-enum34', type='run', when='^python@:2.7')

    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-cligj', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-affine', type=('build', 'run'))
    depends_on('py-snuggs', type=('build', 'run'))
    depends_on('gdal')
    depends_on('jpeg')

    # (Commented out for now: py-boto3 is not yet a Spack package)
    # Some (optional) tests use py-boto3 for Amazon Web Services
    # depends_on('py-boto3', type=('build', 'run'), when='+aws')
