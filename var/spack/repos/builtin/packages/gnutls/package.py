# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Gnutls(AutotoolsPackage):
    """GnuTLS is a secure communications library implementing the SSL, TLS
    and DTLS protocols and technologies around them. It provides a simple C
    language application programming interface (API) to access the secure
    communications protocols as well as APIs to parse and write X.509, PKCS
    #12, OpenPGP and other required structures. It is aimed to be portable
    and efficient with focus on security and interoperability."""

    homepage = "http://www.gnutls.org"
    url      = "https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.19.tar.xz"

    version('3.6.8', sha256='aa81944e5635de981171772857e72be231a7e0f559ae0292d2737de475383e83')
    version('3.6.7.1', sha256='881b26409ecd8ea4c514fd3fbdb6fae5fab422ca7b71116260e263940a4bbbad')
    version('3.5.19', sha256='1936eb64f03aaefd6eb16cef0567457777618573826b94d03376bb6a4afadc44')
    version('3.5.13', '4fd41ad86572933c2379b4cc321a0959')
    version('3.5.10', '336c03a71ba90184ffd0388075dde504')
    version('3.5.9',  '0ab25eb6a1509345dd085bc21a387951')
    version('3.3.9',  'ff61b77e39d09f1140ab5a9cf52c58b6')

    variant('zlib', default=True, description='Enable zlib compression support')
    variant('guile', default=False, description='Enable Guile bindings')

    # gnutls+guile is currently broken on MacOS.  See Issue #11668
    conflicts('+guile', when='platform=darwin')

    # Note that version 3.3.9 of gnutls doesn't support nettle 3.0.
    depends_on('nettle@3.4.1:', when='@3.6.7.1:')
    depends_on('guile', when='+guile')
    depends_on('nettle@:2.9', when='@3.3.9')
    depends_on('nettle', when='@3.5:')
    depends_on('libidn2@:2.0.99', when='@:3.5.99')
    depends_on('zlib', when='+zlib')
    depends_on('gettext')

    depends_on('pkgconfig', type='build')

    build_directory = 'spack-build'

    def url_for_version(self, version):
        url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v{0}/gnutls-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_environment(self, build_env, run_env):
        spec = self.spec
        if '+guile' in spec:
            build_env.set('GUILE', os.path.join(spec["guile"].prefix.bin,
                                                'guile'))

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

        if '+guile' in spec:
            args.append('--enable-guile')
        else:
            args.append('--disable-guile')

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
