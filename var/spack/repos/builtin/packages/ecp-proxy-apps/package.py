# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://exascaleproject.github.io/proxy-apps"
    # Dummy url
    url = 'https://github.com/exascaleproject/proxy-apps/archive/v1.0.tar.gz'

    version('2.0', sha256='5f3cb3a772224e738c1dab42fb34d40f6b313af51ab1c575fb334e573e41e09a')
    version('1.1', '15825c318acd3726fd8e72803b1c1090')
    version('1.0', '8b3f00f05e6cde88d8d913da4293ee62')

    # Added with release 2.0
    depends_on('ember@1.0.0', when='@2.0:')
    depends_on('miniqmc@0.4.0', when='@2.0:')
    depends_on('minivite@1.0', when='@2.0:')
    depends_on('picsarlite@0.1', when='@2.0:')
    depends_on('thornado-mini@1.0', when='@2.0:')

    depends_on('amg@1.1', when='@2.0:')
    depends_on('candle-benchmarks@0.1', when='@2.0:')
    depends_on('laghos@1.1', when='@2.0:')
    depends_on('macsio@1.1', when='@2.0:')
    depends_on('miniamr@1.4.1', when='@2.0:')
    depends_on('sw4lite@1.1', when='@2.0:')
    depends_on('xsbench@18', when='@2.0:')

    # Added with release 1.1
    depends_on('examinimd@1.0', when='@1.1:')

    depends_on('nekbone@17.0', when='@1.0:')
    depends_on('swfft@1.0', when='@1.0:')

    # Dependencies for versions 1.0:1.1
    depends_on('amg@1.0', when='@1.0:1.1')
    depends_on('candle-benchmarks@0.0', when='@1.0:1.1')
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
