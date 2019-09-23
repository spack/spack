# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openldap(AutotoolsPackage):
    """
    OpenLDAP Software is an open source implementation of the Lightweight
    Directory Access Protocol. The suite includes:

    slapd - stand-alone LDAP daemon (server)
    libraries implementing the LDAP protocol, and
    utilities, tools, and sample clients.
    """

    homepage = "https://www.openldap.org/"
    url      = "ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-2.4.9.tgz"

    version('2.4.48', sha256='d9523ffcab5cd14b709fcf3cb4d04e8bc76bb8970113255f372bc74954c6074d')

    variant('client_only', default=True, description='Client only installation')
    variant('icu', default=False, description='Build with unicode support')
    variant('openssl', default=False, description='Use OpenSSL for TLS support')
    variant('perl_backend', default=False, description='Perl backend to Slapd')

    depends_on('icu4c', when='+icu')
    depends_on('gnutls', when='~client_only~openssl')
    depends_on('unixodbc', when='~client_only')
    depends_on('postgresql', when='~client_only')
    depends_on('berkeley-db', when='~client_only')  # for slapd
    # Recommended dependencies by Linux From Scratch
    # depends_on('cyrus-sasl', when='~client_only') # not avail. in spack yet
    # depends_on('openslp', when='~client_only') # not avail. in spack yet
    # depends_on('Pth', when='~client_only') # not avail. in spack yet
    depends_on('perl', when='+perl_backend')  # for slapd

    # Ref: http://www.linuxfromscratch.org/blfs/view/svn/server/openldap.html
    @when('+client_only')
    def configure_args(self):
        return ['CPPFLAGS=-D_GNU_SOURCE',
                '--disable-static',
                '--enable-dynamic',
                '--disable-debug',
                '--disable-slapd',
                ]

    @when('~client_only')
    def configure_args(self):
        # Ref: https://www.openldap.org/lists/openldap-technical/201009/msg00304.html
        args = ['CPPFLAGS=-D_GNU_SOURCE',  # fixes a build error
                '--disable-static',
                '--disable-debug',
                '--with-cyrus-sasl',
                '--enable-dynamic',
                '--enable-crypt',
                '--enable-spasswd',
                '--enable-slapd',
                '--enable-modules',
                '--enable-rlookups',
                '--enable-backends=mod',
                '--disable-ndb',
                '--disable-sql',
                '--disable-shell',
                '--disable-bdb',
                '--disable-hdb',
                '--enable-overlays=mod',
                ]

        if when('~openssl'):
            args.append('--with-tls=gnutls')
        else:
            args.append('--with-tls=openssl')

        if '+perl_backend' in self.spec:
            args.append('--enable-perl')
        else:
            args.append('--disable-perl')

        return args

    def install(self, spec, prefix):
        make('depend')
        make()
        make('install')
