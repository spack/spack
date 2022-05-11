# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Libssh2(CMakePackage):
    """libssh2 is a client-side C library implementing the SSH2 protocol"""

    homepage = "https://www.libssh2.org/"
    url      = "https://www.libssh2.org/download/libssh2-1.7.0.tar.gz"

    version('1.10.0', sha256='2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51')
    version('1.9.0',  sha256='d5fb8bd563305fd1074dda90bd053fb2d29fc4bce048d182f96eaa466dfadafd')
    version('1.8.0', sha256='39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4')
    version('1.7.0', sha256='e4561fd43a50539a8c2ceb37841691baf03ecb7daf043766da1b112e4280d584')
    version('1.4.3', sha256='eac6f85f9df9db2e6386906a6227eb2cd7b3245739561cad7d6dc1d5d021b96d')  # CentOS7

    variant('crypto', default='openssl', values=('openssl', 'mbedtls'), multi=False)
    variant('shared', default=True, description="Build shared libraries")

    conflicts('crypto=mbedtls', when='@:1.7', msg='mbedtls only available from 1.8.0')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('openssl', when='crypto=openssl')
    depends_on('openssl@:2', when='@:1.9 crypto=openssl')
    depends_on('mbedtls@:2 +pic', when='crypto=mbedtls')
    depends_on('zlib')
    depends_on('xz')

    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', 'OFF'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared')
        ]

        crypto = self.spec.variants['crypto'].value

        if crypto == 'openssl':
            args.append(self.define('CRYPTO_BACKEND', 'OpenSSL'))
        elif crypto == 'mbedtls':
            args.append(self.define('CRYPTO_BACKEND', 'mbedTLS'))

        return args

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies('platform=darwin'):
            fix_darwin_install_name(self.prefix.lib)

    def check(self):
        # Docker is required to run tests
        if which('docker'):
            make('test')
