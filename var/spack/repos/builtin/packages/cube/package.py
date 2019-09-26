# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cube(AutotoolsPackage):
    """Cube the profile viewer for Score-P and Scalasca profiles. It displays a
    multi-dimensional performance space consisting of the dimensions:
    - performance metric
    - call path
    - system resource
    """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url      = "http://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubegui-4.4.2.tar.gz"

    version('4.4.4', '9b7b96d5a64b558a9017cc3599bba93a42095534e018e3de9b1f80ab6d04cc34')
    version('4.4.3', 'bf4b0f2ff68507ff82ba24eb4895aed961710dae16d783c222a12f152440cf36')
    version('4.4.2', '29b6479616a524f8325f5031a883963bf965fb92569de33271a020f08650ec7b')
    version('4.4',   '0620bae3ac357d0486ce7f5f97e448eeb2494c9a31865b679380ee08c6750e70')
    version('4.3.5', 'e5dce986e3c6381ea3a5fcb66c553adc')
    version('4.3.4', '50f73060f55311cb12c5b3cb354d59fa')
    version('4.3.3', '07e109248ed8ffc7bdcce614264a2909')
    version('4.2.3', '8f95b9531f5a8f8134f279c2767c9b20')

    variant('gui', default=True, description='Build Cube GUI')

    patch('qt-version.patch', when='@4.3.0:4.3.999 +gui')

    depends_on('cubelib', when='@4.4:')

    depends_on('pkgconfig', type='build')
    depends_on('dbus')
    depends_on('zlib')

    depends_on('qt@5:', when='@4.3.0: +gui')
    depends_on('qt@4.8:', when='@4.2.0:4.2.999 +gui')

    conflicts('~gui', when='@4.4:')

    def url_for_version(self, version):
        if version >= Version('4.4'):
            url = 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubegui-{1}.tar.gz'
        else:
            url = 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cube-{1}.tar.gz'

        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec

        configure_args = ['--enable-shared']

        if '+gui' not in spec:
            configure_args.append('--without-gui')

        return configure_args

    def install(self, spec, prefix):
        make('install', parallel=False)
