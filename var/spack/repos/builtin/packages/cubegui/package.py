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

    version('4.4', '0ade1cd54636e6c85efba1a4a6af0068 ')

    depends_on('cubelib@4.4:')
    depends_on('qt@4.6:')

    def url_for_version(self, version):
        filename = 'cubegui-{0}.tar.gz'.format(version)

        return 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/{1}'.format(version.up_to(2), filename)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('QT_PATH', '$QTDIR')

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
