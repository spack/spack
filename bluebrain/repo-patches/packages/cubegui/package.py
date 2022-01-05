##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cubegui(AutotoolsPackage):
    """CubeGUI Graphical explorer is the the GUI component of
    Cube the profile viewer for Score-P and Scalasca profiles. It displays a
    multi-dimensional performance space consisting of the dimensions:
    - performance metric
    - call path
    - system resource
    """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url = "http://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubegui-4.4.tar.gz"

    version('4.4', sha256='0620bae3ac357d0486ce7f5f97e448eeb2494c9a31865b679380ee08c6750e70')

    depends_on('cubelib@4.4:')
    depends_on('qt@4.6:')

    def url_for_version(self, version):
        filename = 'cubegui-{0}.tar.gz'.format(version)

        return 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/{1}'.format(version.up_to(2), filename)

    def setup_build_environment(self, env):
        env.set('QT_PATH', '$QTDIR')

    def configure_args(self):
        spec = self.spec

        configure_args = ['--enable-shared']

        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')
        elif spec.satisfies('%pgi'):
            configure_args.append('--with-nocross-compiler-suite=pgi')
        elif spec.satisfies('%clang'):
            configure_args.append('--with-nocross-compiler-suite=clang')

        return configure_args

    def install(self, spec, prefix):
        make('install', parallel=False)
