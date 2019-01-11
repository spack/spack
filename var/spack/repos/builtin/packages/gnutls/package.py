# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnutls(AutotoolsPackage):
    """GnuTLS is a secure communications library implementing the SSL, TLS
    and DTLS protocols and technologies around them. It provides a simple C
    language application programming interface (API) to access the secure
    communications protocols as well as APIs to parse and write X.509, PKCS
    #12, OpenPGP and other required structures. It is aimed to be portable
    and efficient with focus on security and interoperability."""

    homepage = "http://www.gnutls.org"
    url      = "https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.13.tar.xz"

    version('3.5.13', '4fd41ad86572933c2379b4cc321a0959')
    version('3.5.10', '336c03a71ba90184ffd0388075dde504')
    version('3.5.9',  '0ab25eb6a1509345dd085bc21a387951')
    version('3.3.9',  'ff61b77e39d09f1140ab5a9cf52c58b6')

    variant('zlib', default=True, description='Enable zlib compression support')

    # Note that version 3.3.9 of gnutls doesn't support nettle 3.0.
    depends_on('nettle@:2.9', when='@3.3.9')
    depends_on('nettle', when='@3.5:')
    depends_on('zlib', when='+zlib')
    depends_on('gettext')

    depends_on('pkgconfig', type='build')

    build_directory = 'spack-build'

    def url_for_version(self, version):
        url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v{0}/gnutls-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-static',
        ]

        if spec.satisfies('@3.5:'):
            # use shipped libraries, might be turned into variants
            args.append('--with-included-libtasn1')
            args.append('--with-included-unistring')
            args.append('--without-p11-kit')  # p11-kit@0.23.1: ...

        if '+zlib' in spec:
            args.append('--with-zlib')
        else:
            args.append('--without-zlib')

        if self.run_tests:
            args.extend([
                '--enable-tests',
                '--enable-valgrind-tests',
                '--enable-full-test-suite',
            ])
        else:
            args.extend([
                '--disable-tests',
                '--disable-valgrind-tests',
                '--disable-full-test-suite',
            ])

        return args
