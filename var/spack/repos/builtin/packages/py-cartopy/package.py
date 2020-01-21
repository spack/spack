# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCartopy(PythonPackage):
    """Cartopy - a cartographic python library with matplotlib support."""

    homepage = "http://scitools.org.uk/cartopy/"
    url      = "https://github.com/SciTools/cartopy/archive/v0.16.0.tar.gz"

    version('0.17.0', sha256='137642e63952404ec0841fa0333ad14c58fbbf19cca2a5ac6a38498c4b4998fb')
    version('0.16.0', sha256='cadf62434492c965220b37f0548bc58180466ad6894a1db57dbc51cd43467e5c')

    depends_on('py-setuptools@0.7.2:', type='build')
    depends_on('py-cython@0.15.1:',    type='build')
    depends_on('py-numpy@1.10.0:',  type=('build', 'run'))
    depends_on('py-shapely@1.5.6:', type=('build', 'run'))
    depends_on('py-pyshp@1.1.4:',   type=('build', 'run'))
    depends_on('py-six@1.3.0:',     type=('build', 'run'))
    depends_on('geos@3.3.3:')
    depends_on('proj@4.9.0:5', when='@0.16.0')
    depends_on('proj@4.9:',    when='@0.17.0')

    variant('epsg', default=True, description='Add support for epsg.io')
    variant('ows', default=True, description='Add support for Open Geospatial Consortium (OGC) web service')
    variant('plotting', default=True, description='Add plotting functionality')

    # optional dependecies
    depends_on('py-matplotlib@1.5.1:', type=('build', 'run'), when='+plotting')
    depends_on('gdal@1.10.0:+python',  type=('build', 'run'), when='+plotting')
    depends_on('py-pillow@1.7.8:',     type=('build', 'run'), when='+ows')
    depends_on('py-pillow@1.7.8:',     type=('build', 'run'), when='+plotting')
    depends_on('py-pyepsg@0.2.0:',     type=('build', 'run'), when='+epsg')
    depends_on('py-scipy@0.10:',       type=('build', 'run'), when='+plotting')
    depends_on('py-owslib@0.8.11:',    type=('build', 'run'), when='+ows')

    # testing dependencies
    depends_on('py-filelock',      type='test')
    depends_on('py-mock@1.0.1',    type='test')
    depends_on('py-pytest@3.0.0:', type='test')

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        args = ['-I{0}'.format(spec['proj'].prefix.include),
                '-L{0}'.format(spec['proj'].prefix.lib)
                ]

        if spec.satisfies('@0.17.0 ^proj@6'):
            args.append('-DACCEPT_USE_OF_DEPRECATED_PROJ_API_H')

        return args
