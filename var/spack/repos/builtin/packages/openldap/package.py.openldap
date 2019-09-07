# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openldap(AutotoolsPackage):
    """
    penLDAP Software is an open source implementation of the Lightweight Directory Access Protocol.
    The suite includes:

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

    depends_on('icu4c', when='+icu')
    depends_on('gnutls', when='~client_only~openssl')
    depends_on('unixodbc', when='~client_only')
    depends_on('postgresql', when='~client_only')
    depends_on('berkeley-db', when='~client_only') # for slapd
    # depends_on('cyrus-sasl', when='~client_only') # not avail. in spack yet
    # depends_on('openslp', when='~client_only') # not avail. in spack yet
    # depends_on('Pth', when='~client_only') # not avail. in spack yet

    # Ref: http://www.linuxfromscratch.org/blfs/view/svn/server/openldap.html
    @when('+client_only')
    def configure_args(self):
        args = []
        args.append('CPPFLAGS=-D_GNU_SOURCE')
        args.append('--disable-static')
        args.append('--enable-dynamic')
        args.append('--disable-debug')
        args.append('--disable-slapd')
        return args

    @when('~client_only')
    def configure_args(self):
        args = []
        # Ref: https://www.openldap.org/lists/openldap-technical/201009/msg00304.html
        args.append('CPPFLAGS=-D_GNU_SOURCE') # fixes a build error
        args.append('--disable-static')
        args.append('--disable-debug')
        if when('~openssl'):
            args.append('--with-tls=gnutls')
        else:
            args.append('--with-tls=openssl')
        args.append('--with-cyrus-sasl')
        args.append('--enable-dynamic')
        args.append('--enable-crypt')
        args.append('--enable-spasswd')
        args.append('--enable-slapd')
        args.append('--enable-modules')
        args.append('--enable-rlookups')
        args.append('--enable-backends=mod')
        args.append('--disable-ndb')
        args.append('--disable-sql')
        args.append('--disable-shell')
        args.append('--disable-bdb')
        args.append('--disable-hdb')
        args.append('--enable-overlays=mod')
        return args


    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make('depend')
        make()
        make('install')
