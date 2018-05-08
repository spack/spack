##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
