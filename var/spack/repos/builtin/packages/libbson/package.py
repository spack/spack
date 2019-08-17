# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbson(AutotoolsPackage):
    """libbson is a library providing useful routines related to building,
    parsing, and iterating BSON documents."""

    homepage = "https://github.com/mongodb/libbson"
    url      = "https://github.com/mongodb/libbson/releases/download/1.7.0/libbson-1.7.0.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.9.1', 'f91f59fc5a0cbba94d4d32dad1bd0cfd')
    version('1.8.1', '42601455cf7f450b46f62c4e6115c440')
    version('1.8.0', '8b3c64570eec721f951831958e707a5a')
    version('1.7.0', 'e196ad77dd8458ebc1166e6135030b63')
    version('1.6.3', 'b7bdb314197106fcfb4af105a582d343')
    version('1.6.2', 'c128a2ae3e35295e1176465be60f19db')
    version('1.6.1', '4d6779451bc5764a7d4982c01e7bd8c2')

    depends_on('autoconf', type='build', when='@1.6.1')
    depends_on('automake', type='build', when='@1.6.1')
    depends_on('libtool', type='build', when='@1.6.1')
    depends_on('m4', type='build', when='@1.6.1')

    @property
    def force_autoreconf(self):
        # 1.6.1 tarball is broken
        return self.spec.satisfies('@1.6.1')
