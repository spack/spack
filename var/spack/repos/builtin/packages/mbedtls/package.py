# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mbedtls(CMakePackage):
    """mbed TLS (formerly known as PolarSSL) makes it trivially easy for
       developers to include cryptographic and SSL/TLS capabilities in
       their (embedded) products, facilitating this functionality with a
       minimal coding footprint.
    """

    homepage = "https://tls.mbed.org"
    url      = "https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.2.1.tar.gz"

    version('2.16.1', 'daf0d40f3016c34eb42d1e4b3b52be047e976d566aba8668977723c829af72f3')
    version('2.7.10', '42b19b30b86a798bdb69c5da2f8bbd7d72ffede9a35b888ab986a29480f9dc3e')
    version('2.3.0', '98158e1160a0825a3e8db38881a177a0')
    version('2.2.1', '73a38f96898d6d03e32f55dd9f9a67be')
    version('2.2.0', 'eaf4586c1ef93ae872e606b6c1203942')
    version('2.1.4', '40cdf67b6c6d92c9cbcfd552d39ea3ae')
    version('2.1.3', '7eb4cf1dfa68578a2c8dbd0b6fa752dd')
    version('1.3.16', '4144d7320c691f721aeb9e67a1bc38e0')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'Coverage', 'ASan', 'ASanDbg',
                    'MemSan', 'MemSanDbg', 'Check', 'CheckFull'))

    variant('pic', default=False,
            description='Compile with position independent code.')

    depends_on('cmake@2.6:', type='build')
    depends_on('perl', type='build')

    def flag_handler(self, name, flags):

        # Compile with PIC, if requested.
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)

        return (flags, None, None)
