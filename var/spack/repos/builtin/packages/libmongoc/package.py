# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmongoc(AutotoolsPackage):
    """libmongoc is a client library written in C for MongoDB."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url      = "https://github.com/mongodb/mongo-c-driver/releases/download/1.7.0/mongo-c-driver-1.7.0.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.9.5', sha256='4a4bd0b0375450250a3da50c050b84b9ba8950ce32e16555714e75ebae0b8019')
    version('1.9.4', sha256='910c2f1b2e3df4d0ea39c2f242160028f90fcb8201f05339a730ec4ba70811fb')
    version('1.9.3', sha256='c2c94ef63aaa09efabcbadc4ac3c8740faa102266bdd2559d550f1955b824398')
    version('1.9.1', '86f98ace1a5f073eea6875a96761b198')
    version('1.8.1', '52d54a4107a2da20c1a1b28bc1ff9d44')
    version('1.8.0', '8c271a16ff30f6d4f5e134f699f7360f')
    version('1.7.0', '21acf3584e92631422bc91e9e3cf4f76')
    version('1.6.3', '0193610cf1d98aae7008f272a1000972')
    version('1.6.2', 'aac86df153282cda1e4905cca181631a')
    version('1.6.1', '826946de9a15f7f453aefecdc76b1c0d')

    variant('ssl', default=True, description='Enable SSL support.')
    variant('snappy', default=True, description='Enable Snappy support.')
    variant('zlib', default=True, description='Enable zlib support.')

    patch('https://github.com/mongodb/mongo-c-driver/pull/466.patch', sha256='713a872217d11aba04a774785a2824d26b566543c270a1fa386114f5200fda20', when='@1.8.1')

    depends_on('autoconf', type='build', when='@1.8.1')
    depends_on('automake', type='build', when='@1.8.1')
    depends_on('libtool', type='build', when='@1.8.1')
    depends_on('m4', type='build', when='@1.8.1')
    depends_on('pkgconfig', type='build')

    depends_on('libbson')

    depends_on('openssl', when='+ssl')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')

    @property
    def force_autoreconf(self):
        # Run autoreconf due to build system patch
        return self.spec.satisfies('@1.8.1')

    def configure_args(self):
        spec = self.spec

        args = [
            '--disable-automatic-init-and-cleanup'
        ]

        if '+ssl' in spec:
            args.append('--enable-ssl=openssl')
        else:
            args.append('--enable-ssl=no')

        if spec.satisfies('@1.7.0:'):
            # --with-{snappy,zlib}=system are broken for versions < 1.8.1
            if '+snappy' not in spec:
                args.append('--with-snappy=no')
            elif spec.satisfies('@1.8.1:'):
                args.append('--with-snappy=system')

            if '+zlib' not in spec:
                args.append('--with-zlib=no')
            elif spec.satisfies('@1.8.1:'):
                args.append('--with-zlib=system')

        if spec.satisfies('@1.9.3:'):
            args.append('--with-libbson=auto')
        else:
            args.append('--with-libbson=system')
        return args
