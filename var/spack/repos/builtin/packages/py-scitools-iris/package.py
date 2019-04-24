# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScitoolsIris(PythonPackage):
    """A powerful, format-agnostic, community-driven Python library for
    analysing and visualising Earth science data"""

    homepage = "http://scitools.org.uk"
    url      = "https://pypi.io/packages/source/s/scitools-iris/scitools-iris-2.2.0.tar.gz"

    version('2.2.0', sha256='1bf8853f5d7a210f711636d32a52ff62b84a56330fe159720ef56f36f3804ade')

    #depends_on('py-setuptools', type='build')
    depends_on('py-cartopy', type=('build', 'run'))
    depends_on('proj@4:4.99')
    depends_on('py-cf-units', type=('build', 'run'))
    depends_on('py-cftime', type=('build', 'run'))
    depends_on('py-dask', type=('build', 'run'))
    depends_on('py-matplotlib@2:2.99', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
