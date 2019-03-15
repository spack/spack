# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwebsockets(CMakePackage):
    """C library for lightweight websocket clients and servers."""

    homepage = "https://github.com/warmcat/libwebsockets"
    url      = "https://github.com/warmcat/libwebsockets/archive/v3.tar.gz"
    maintainers = ['ax3l']

    variant('libuv', default=False, description='Build with libuv support')

    version('3.1.0', 'db948be74c78fc13f1f1a55e76707d7baae3a1c8f62b625f639e8f2736298324')
    version('3.0.1', 'cb0cdd8d0954fcfd97a689077568f286cdbb44111883e0a85d29860449c47cbf')
    version('2.2.1', '1f641cde2ab3687db3d553f68fe0f620')
    version('2.1.1', '674684ffb90d4a0bcf7a075eb7b90192')
    version('2.1.0', '4df3be57dee43aeebd54a3ed56568f50')
    version('2.0.3', 'a025156d606d90579e65d53ccd062a94')
    version('1.7.9', '7b3692ead5ae00fd0e1d56c080170f07')

    depends_on('zlib')
    depends_on('openssl')
    depends_on('libuv', when='+libuv')

    def cmake_args(self):
        args = ['-DLWS_WITH_SHARED=ON', '-DLWS_WITH_STATIC=OFF',
                '-DLWS_LINK_TESTAPPS_DYNAMIC=ON']
        if 'libuv' in self.spec:
            args += ['-DLWS_WITH_LIBUV=ON']

        return args
