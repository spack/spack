# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack import *
import spack.architecture

import os


class Openssl(Package):   # Uses Fake Autotools, should subclass Package
    """OpenSSL is an open source project that provides a robust,
       commercial-grade, and full-featured toolkit for the Transport
       Layer Security (TLS) and Secure Sockets Layer (SSL) protocols.
       It is also a general-purpose cryptography library."""
    homepage = "http://www.openssl.org"

    # URL must remain http:// so Spack can bootstrap curl
    url = "http://www.openssl.org/source/openssl-1.0.2m.tar.gz"
    list_url = "https://www.openssl.org/source/old/"
    list_depth = 1

    # The latest stable version is the 1.1.1 series. This is also our Long Term
    # Support (LTS) version, supported until 11th September 2023.
    version('1.1.1c', sha256='f6fb3079ad15076154eda9413fed42877d668e7069d9b87396d0804fdb3f4c90')
    version('1.1.1b', sha256='5c557b023230413dfb0756f3137a13e6d726838ccd1430888ad15bfb2b43ea4b')
    version('1.1.1a', sha256='fc20130f8b7cbd2fb918b2f14e2f429e109c31ddd0fb38fc5d71d9ffed3f9f41')
    version('1.1.1',  sha256='2836875a0f89c03d0fdf483941512613a50cfb421d6fd94b9f41d7279d586a3d')

    # The 1.1.0 series is currently only receiving security fixes and will go
    # out of support on 11th September 2019.
    version('1.1.0k', sha256='efa4965f4f773574d6cbda1cf874dbbe455ab1c0d4f906115f867d30444470b1')
    version('1.1.0j', sha256='31bec6c203ce1a8e93d5994f4ed304c63ccf07676118b6634edded12ad1b3246')
    version('1.1.0i', sha256='ebbfc844a8c8cc0ea5dc10b86c9ce97f401837f3fa08c17b2cdadc118253cf99')
    version('1.1.0g', 'ba5f1b8b835b88cadbce9b35ed9531a6')
    version('1.1.0e', '51c42d152122e474754aea96f66928c6')
    version('1.1.0d', '711ce3cd5f53a99c0e12a7d5804f0f63')
    version('1.1.0c', '601e8191f72b18192a937ecf1a800f3f')

    # Our previous LTS version (1.0.2 series) will continue to be supported
    # until 31st December 2019 (security fixes only during the last year of
    # support).
    version('1.0.2s', sha256='cabd5c9492825ce5bd23f3c3aeed6a97f8142f606d893df216411f07d1abab96')
    version('1.0.2r', sha256='ae51d08bba8a83958e894946f15303ff894d75c2b8bbd44a852b64e3fe11d0d6')
    version('1.0.2p', sha256='50a98e07b1a89eb8f6a99477f262df71c6fa7bef77df4dc83025a2845c827d00')
    version('1.0.2o', '44279b8557c3247cbe324e2322ecd114')
    version('1.0.2n', '13bdc1b1d1ff39b6fd42a255e74676a4')
    version('1.0.2m', '10e9e37f492094b9ef296f68f24a7666')
    version('1.0.2k', 'f965fc0bf01bf882b31314b61391ae65')
    version('1.0.2j', '96322138f0b69e61b7212bc53d5e912b')
    version('1.0.2i', '678374e63f8df456a697d3e5e5a931fb')
    version('1.0.2h', '9392e65072ce4b614c1392eefc1f23d0')
    version('1.0.2g', 'f3c710c045cdee5fd114feb69feba7aa')
    version('1.0.2f', 'b3bf73f507172be9292ea2a8c28b659d')
    version('1.0.2e', '5262bfa25b60ed9de9f28d5d52d77fc5')
    version('1.0.2d', '38dd619b2e77cbac69b99f52a053d25a')

    # The 1.0.1 version is now out of support and should not be used.
    version('1.0.1u', '130bb19745db2a5a09f22ccbbf7e69d0')
    version('1.0.1t', '9837746fcf8a6727d46d22ca35953da1')
    version('1.0.1r', '1abd905e079542ccae948af37e393d28')
    version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
    version('1.0.1e', '66bf6f10f060d561929de96f9dfe5b8c')

    variant('systemcerts', default=True, description='Use system certificates')

    depends_on('zlib')

    depends_on('perl@5.14.0:', type=('build', 'test'))

    parallel = False

    @property
    def libs(self):
        return find_libraries(['libssl', 'libcrypto'], root=self.prefix.lib)

    def handle_fetch_error(self, error):
        tty.warn("Fetching OpenSSL failed. This may indicate that OpenSSL has "
                 "been updated, and the version in your instance of Spack is "
                 "insecure. Consider updating to the latest OpenSSL version.")

    def install(self, spec, prefix):
        # OpenSSL uses a variable APPS in its Makefile. If it happens to be set
        # in the environment, then this will override what is set in the
        # Makefile, leading to build errors.
        env.pop('APPS', None)

        if str(spec.target.family) in ('x86_64', 'ppc64'):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env['KERNEL_BITS'] = '64'

        options = ['zlib', 'shared']
        if spec.satisfies('@1.0'):
            options.append('no-krb5')
        # clang does not support the .arch directive in assembly files.
        if 'clang' in self.compiler.cc and \
           'aarch64' in spack.architecture.sys_type():
            options.append('no-asm')

        config = Executable('./config')
        config('--prefix=%s' % prefix,
               '--openssldir=%s' % join_path(prefix, 'etc', 'openssl'),
               '-I{0}'.format(self.spec['zlib'].prefix.include),
               '-L{0}'.format(self.spec['zlib'].prefix.lib),
               *options)

        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r'-arch x86_64', '', 'Makefile')

        make()
        if self.run_tests:
            make('test')            # 'VERBOSE=1'
        make('install')

    @run_after('install')
    def link_system_certs(self):
        if '+systemcerts' not in self.spec:
            return

        system_dirs = [
            # CentOS, Fedora, RHEL
            '/etc/pki/tls',
            # Ubuntu
            '/usr/lib/ssl',
            # OpenSUSE
            '/etc/ssl'
        ]

        pkg_dir = join_path(self.prefix, 'etc', 'openssl')

        for directory in system_dirs:
            sys_cert = join_path(directory, 'cert.pem')
            pkg_cert = join_path(pkg_dir, 'cert.pem')
            # If a bundle exists, use it. This is the preferred way on Fedora,
            # where the certs directory does not work.
            if os.path.exists(sys_cert) and not os.path.exists(pkg_cert):
                os.symlink(sys_cert, pkg_cert)

            sys_certs = join_path(directory, 'certs')
            pkg_certs = join_path(pkg_dir, 'certs')
            # If the certs directory exists, symlink it into the package.
            # We symlink the whole directory instead of all files because
            # the directory contents might change without Spack noticing.
            if os.path.isdir(sys_certs) and not os.path.islink(pkg_certs):
                os.rmdir(pkg_certs)
                os.symlink(sys_certs, pkg_certs)
