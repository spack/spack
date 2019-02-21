# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Curl(AutotoolsPackage):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "http://curl.haxx.se"
    # URL must remain http:// so Spack can bootstrap curl
    url      = "http://curl.haxx.se/download/curl-7.60.0.tar.bz2"

    version('7.63.0', sha256='9bab7ed4ecff77020a312d84cc5fb7eb02d58419d218f267477a724a17fd8dd8')
    version('7.60.0', 'bd2aabf78ded6a9aec8a54532fd6b5d7')
    version('7.59.0', 'a2192804f7c2636a09320416afcf888e')
    version('7.56.0', 'e0caf257103e0c77cee5be7e9ac66ca4')
    version('7.54.0', '89bb7ba87384dfbf4f1a3f953da42458')
    version('7.53.1', 'fb1f03a142236840c1a77c035fa4c542')
    version('7.52.1', 'dd014df06ff1d12e173de86873f9f77a')
    version('7.50.3', 'bd177fd6deecce00cfa7b5916d831c5e')
    version('7.50.2', '6e161179f7af4b9f8b6ea21420132719')
    version('7.50.1', '015f6a0217ca6f2c5442ca406476920b')
    version('7.49.1', '6bb1f7af5b58b30e4e6414b8c1abccab')
    version('7.47.1', '9ea3123449439bbd960cd25cf98796fb')
    version('7.46.0', '9979f989a2a9930d10f1b3deeabc2148')
    version('7.45.0', '62c1a352b28558f25ba6209214beadc8')
    version('7.44.0', '6b952ca00e5473b16a11f05f06aa8dae')
    version('7.43.0', '11bddbb452a8b766b932f859aaeeed39')
    version('7.42.1', '296945012ce647b94083ed427c1877a8')

    # =================== Variants for Optional Dependencies
    # http://www.linuxfromscratch.org/blfs/view/cvs/basicnet/curl.html

    # c-ares: A C library for asynchronous DNS requests
    variant('cares', default=False, description='Use c-cares library')
    # GnuTLS is a secure communications library implementing the SSL,
    # TLS and DTLS protocols and technologies around them.
    variant('gnutls', default=False, description='Use GNU TLS library')
    # libssh: the SSH library"""
    variant('libssh',     default=False, description='use libssh library')  # , when='7.58:')
    # libssh2 is a client-side C library implementing the SSH2 protocol
    variant('libssh2',    default=True, description='use libssh2 library')
    # nghttp2 is an implementation of HTTP/2 and its header
    # compression algorithm HPACK in C.
    variant('nghttp2',    default=False, description='use nghttp2 library (requires C++11)')

    # mbed TLS (formerly known as PolarSSL) makes it trivially easy
    # for developers to include cryptographic and SSL/TLS capabilities
    variant('mbedtls', default=False, description='Use mbed TLS library')

    variant('darwinssl',  default=sys.platform == 'darwin',
            description="use Apple's SSL/TLS implementation")

    # ================ Conflicts
    conflicts('+libssh', when='@:7.57.99')
    # on OSX and --with-ssh the configure steps fails with
    # one or more libs available at link-time are not available run-time
    # unless the libssh are installed externally (e.g. via homebrew), even
    # though spack isn't supposed to know about such a libssh installation.
    # C.f. https://github.com/spack/spack/issues/7777
    conflicts('platform=darwin', when='+libssh2')
    conflicts('platform=darwin', when='+libssh')
    conflicts('platform=linux', when='+darwinssl')

    # =================
    depends_on('zlib')
    depends_on('cares', when='+cares')
    depends_on('gnutls', when='+gnutls')
    depends_on('libssh', when='+libssh')
    depends_on('libssh2', when='+libssh2')
    depends_on('nghttp2', when='+nghttp2')
    depends_on('mbedtls', when='+mbedtls')
    depends_on('openssl', when='~darwinssl')

    def configure_args(self):
        spec = self.spec

        args = []

        # Same order as ./configure --help
        args += ['--with-zlib={0}'.format(spec['zlib'].prefix)]
        args.append('--without-brotli')
        args += ['--disable-ldap', '--disable-ldaps']
        args.append('--without-winssl')

        if spec.satisfies('+darwinssl'):
            args.append('--with-darwinssl')
        else:
            args.append('--with-ssl={0}'.format(spec['openssl'].prefix))

        args += self.with_or_without('gnutls')
        args.append('--without-polarssl')
        args += self.with_or_without('mbedtls')
        args.append('--without-cyassl')
        args.append('--without-wolfssl')
        args.append('--without-nss')
        args.append('--without-axtls')
        args.append('--without-libmetalink')
        args += self.with_or_without('libssh2')
        args += self.with_or_without('libssh')
        args.append('--without-librtmp')
        args.append('--without-winidn')
        args.append('--without-libidn2')
        args += self.with_or_without('nghttp2')

        return args
