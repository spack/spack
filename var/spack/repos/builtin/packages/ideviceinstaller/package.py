# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ideviceinstaller(Package):
    """Cross-platform library for communicating with iOS devices."""

    homepage = "https://www.libimobiledevice.org/"
    url      = "https://www.libimobiledevice.org/downloads/ideviceinstaller-1.1.0.tar.bz2"
    git      = "https://git.libimobiledevice.org/ideviceinstaller.git"

    version('master', branch='master')
    version('1.1.0',  sha256='0821b8d3ca6153d9bf82ceba2706f7bd0e3f07b90a138d79c2448e42362e2f53')
    version('1.0.1',  sha256='e2e5dc41c08cce7cec9edaf4596322f424d5195c255d3c1b957b81b45529b4f5')
    version('1.0.0',  sha256='6d781621e0823275b22cfbcfb13f2707d4630da040744acca77ed987d0928d86')

    depends_on('autoconf', when='@master')
    depends_on('automake', when='@master')
    depends_on('libtool',  when='@master')
    depends_on('libimobiledevice')
    depends_on('libzip')
    depends_on('pkg-config')

    def install(self, spec, prefix):
        if self.spec.satisfies('@master'):
            autogen = Executable('./autogen.sh')
            autogen()
        configure('--disable-dependency-tracking',
                  '--prefix=%s' % self.spec.prefix)
        make('install')
