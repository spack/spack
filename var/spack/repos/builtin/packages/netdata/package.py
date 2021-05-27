# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Netdata(AutotoolsPackage):
    """Real-time performance monitoring, done right!"""

    homepage = "https://www.netdata.cloud/"
    url      = "https://github.com/netdata/netdata/releases/download/v1.30.1/netdata-v1.30.1.tar.gz"

    version('1.30.1', sha256='3df188ac04f17094cb929e2990841ba77f68aa6af484e0509b99db298fa206c9')
    version('1.22.1', sha256='f169c8615a6823448c2f1923c87c286d798132ea29d26f366e96d26e0aec3697')

    depends_on('pkgconfig', type='build')
    depends_on('libuv')
    depends_on('uuid')
    depends_on('zlib')

    @run_after('install')
    def setup_dirs(self):
        # netdata requires the following directories to be able to run.
        mkdirp(self.prefix.var.cache.netdata)
        mkdirp(self.prefix.var.lib.netdata)
        mkdirp(self.prefix.var.log.netdata)
