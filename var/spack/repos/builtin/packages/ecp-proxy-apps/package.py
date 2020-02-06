# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *


class EcpProxyApps(Package):
    """This is a collection of packages that represents the official suite of
       DOE/ECP proxy applications. This is a Spack bundle package that
       installs the ECP proxy application suite.
    """

    tags = ['proxy-app', 'ecp-proxy-app']
    maintainers = ['bhatele']

    homepage = "https://proxyapps.exascaleproject.org"
    # Dummy url
    url = 'https://github.com/exascaleproject/proxy-apps/archive/v1.0.tar.gz'

    version('2.1', sha256='604da008fc4ef3bdbc25505088d610333249e3e9745eac7dbfd05b91e33e218d')
    version('2.0', sha256='5f3cb3a772224e738c1dab42fb34d40f6b313af51ab1c575fb334e573e41e09a')
    version('1.1', sha256='8537e03588c0f46bebf5b7f07146c79812f2ebfb77d29e184baa4dd5f4603ee3')
    version('1.0', sha256='13d9795494dabdb4c724d2c0f322c2149b2507d2fd386ced12b54292b7ecf595')

    variant('candle', default=False,
            description='Also build CANDLE Benchmarks')

    # Added with release 2.1
    depends_on('amg@1.2', when='@2.1:')
    depends_on('miniamr@1.4.3', when='@2.1:')

    # Added with release 2.0
    depends_on('ember@1.0.0', when='@2.0:')
    depends_on('miniqmc@0.4.0', when='@2.0:')
    depends_on('minivite@1.0', when='@2.0:')
    depends_on('picsarlite@0.1', when='@2.0:')
    depends_on('thornado-mini@1.0', when='@2.0:')

    depends_on('candle-benchmarks@0.1', when='+candle @2.0:')
    depends_on('laghos@2.0', when='@2.0:')
    depends_on('macsio@1.1', when='@2.0:')
    depends_on('sw4lite@1.1', when='@2.0:')
    depends_on('xsbench@18', when='@2.0:')

    # Dependencies for version 2.0
    depends_on('amg@1.1', when='@2.0')
    depends_on('miniamr@1.4.1', when='@2.0')

    # Added with release 1.1
    depends_on('examinimd@1.0', when='@1.1:')

    depends_on('nekbone@17.0', when='@1.0:')
    depends_on('swfft@1.0', when='@1.0:')

    # Dependencies for versions 1.0:1.1
    depends_on('amg@1.0', when='@1.0:1.1')
    depends_on('candle-benchmarks@0.0', when='+candle @1.0:1.1')
    depends_on('laghos@1.0', when='@1.0:1.1')
    depends_on('macsio@1.0', when='@1.0:1.1')
    depends_on('miniamr@1.4.0', when='@1.0:1.1')
    depends_on('sw4lite@1.0', when='@1.0:1.1')
    depends_on('xsbench@14', when='@1.0:1.1')

    # Removed after release 1.1
    depends_on('minife@2.1.0', when='@1.0:1.1')
    depends_on('minitri@1.0', when='@1.0:1.1')

    # Removed after release 1.0
    depends_on('comd@1.1', when='@1.0')

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        with open(os.path.join(spec.prefix, 'package-list.txt'), 'w') as out:
            for dep in spec.dependencies(deptype='build'):
                out.write("%s\n" % dep.format(
                    format_string='${PACKAGE} ${VERSION}'))
                os.symlink(dep.prefix, os.path.join(spec.prefix, dep.name))
            out.close()
