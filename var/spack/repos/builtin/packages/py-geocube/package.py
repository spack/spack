# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGeocube(PythonPackage):
    """Tool to convert geopandas vector data into rasterized xarray data."""

    homepage = "https://github.com/corteva/geocube"
    pypi     = "geocube/geocube-0.0.17.tar.gz"

    maintainers = ['adamjstewart']

    version('0.0.17', sha256='bf8da0fa96d772ebaea0b98bafa0ba5b8639669d5feb07465d4255af177bddc0')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-click@6.0:', type=('build', 'run'))
    depends_on('py-datacube', type=('build', 'run'))
    depends_on('py-geopandas@0.7:', type=('build', 'run'))
    depends_on('py-rasterio', type=('build', 'run'))
    depends_on('py-rioxarray@0.4:', type=('build', 'run'))
    depends_on('py-xarray@0.17:', type=('build', 'run'))
    depends_on('py-pyproj@2:', type=('build', 'run'))
