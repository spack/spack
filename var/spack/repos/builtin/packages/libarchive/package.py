# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "https://www.libarchive.org"
    url      = "https://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"
    maintainers = ['haampie']

    version('3.5.2', sha256='5f245bd5176bc5f67428eb0aa497e09979264a153a074d35416521a5b8e86189')
    version('3.5.1', sha256='9015d109ec00bb9ae1a384b172bf2fc1dff41e2c66e5a9eeddf933af9db37f5a')
    version('3.4.1', sha256='fcf87f3ad8db2e4f74f32526dee62dd1fb9894782b0a503a89c9d7a70a235191')
    version('3.3.2', sha256='ed2dbd6954792b2c054ccf8ec4b330a54b85904a80cef477a1c74643ddafa0ce')
    version('3.2.1', sha256='72ee1a4e3fd534525f13a0ba1aa7b05b203d186e0c6072a8a4738649d0b3cfd2')
    version('3.1.2', sha256='eb87eacd8fe49e8d90c8fdc189813023ccc319c5e752b01fb6ad0cc7b2c53d5e')
    version('3.1.1', sha256='4968f9a3f2405ec7e07d5f6e78b36f21bceee6196df0a795165f89774bbbc6d8')
    version('3.1.0', sha256='64b15dfa623b323da8fc9c238b5bca962ec3b38dcdfd2ed86f5f509e578a3524')

    variant('libs', default='static,shared', values=('static', 'shared'),
            multi=True, description='What libraries to build')

    # TODO: BLAKE2 is missing
    variant('compression', default='bz2lib,lz4,lzo2,lzma,zlib,zstd', values=('bz2lib', 'lz4', 'lzo2', 'lzma', 'zlib', 'zstd'), multi=True, description='Supported compression')
    variant('xar', default='libxml2', values=('libxml2', 'expat'), description='What library to use for xar support')
    variant('crypto', default='mbedtls', values=('mbedtls', 'nettle', 'openssl'), description='What crypto library to use for mtree and xar hashes')
    variant('programs', values=any_combination_of('bsdtar', 'bsdcpio', 'bsdcat'), description='What executables to build')
    variant('iconv', default=True, description='Support iconv')

    depends_on('bzip2', when='compression=bz2lib')
    depends_on('lz4', when='compression=lz4')
    depends_on('lzo', when='compression=lzo2')
    depends_on('xz', when='compression=lzma')
    depends_on('zlib', when='compression=zlib')
    depends_on('zstd', when='compression=zstd')

    depends_on('nettle', when='crypto=nettle')
    depends_on('openssl', when='crypto=openssl')
    depends_on('mbedtls@2.0:2 +pic', when='crypto=mbedtls')

    depends_on('libxml2', when='xar=libxml2')
    depends_on('expat', when='xar=expat')

    depends_on('libiconv', when='+iconv')

    conflicts('crypto=mbedtls', when='@:3.4.1', msg="mbed TLS is only supported from libarchive 3.4.2")

    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel

    def configure_args(self):
        args = ['--without-libb2']
        args += self.with_or_without('compression')
        args += self.with_or_without('crypto')
        args += self.with_or_without('iconv')
        args += self.with_or_without('xar')
        args += self.enable_or_disable('programs')

        return args
