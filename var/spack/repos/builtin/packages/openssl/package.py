##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import urllib
import llnl.util.tty as tty

from spack import *


class Openssl(Package):
    """The OpenSSL Project is a collaborative effort to develop a
       robust, commercial-grade, full-featured, and Open Source
       toolkit implementing the Secure Sockets Layer (SSL v2/v3) and
       Transport Layer Security (TLS v1) protocols as well as a
       full-strength general purpose cryptography library."""
    homepage = "http://www.openssl.org"
    url      = "https://www.openssl.org/source/openssl-1.0.1h.tar.gz"

    version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
    version('1.0.1r', '1abd905e079542ccae948af37e393d28')
    version('1.0.1t', '9837746fcf8a6727d46d22ca35953da1')
    version('1.0.2d', '38dd619b2e77cbac69b99f52a053d25a')
    version('1.0.2e', '5262bfa25b60ed9de9f28d5d52d77fc5')
    version('1.0.2f', 'b3bf73f507172be9292ea2a8c28b659d')
    version('1.0.2g', 'f3c710c045cdee5fd114feb69feba7aa')
    version('1.0.2h', '9392e65072ce4b614c1392eefc1f23d0')

    depends_on("zlib")
    parallel = False

    def url_for_version(self, version):
        # This URL is computed pinging the place where the latest version is stored. To avoid slowdown
        # due to repeated pinging, we store the URL in a private class attribute to do the job only once per version
        openssl_urls = getattr(Openssl, '_openssl_url', {})
        openssl_url = openssl_urls.get(version, None)
        # Same idea, but just to avoid issuing the same message multiple times
        warnings_given_to_user = getattr(Openssl, '_warnings_given', {})
        if openssl_url is None:
            if self.spec.satisfies('@external'):
                # The version @external is reserved to system openssl. In that case return a fake url and exit
                openssl_url = '@external (reserved version for system openssl)'
                if not warnings_given_to_user.get(version, False):
                    tty.msg('Using openssl@external : the version @external is reserved for system openssl')
                    warnings_given_to_user[version] = True
            else:
                openssl_url = self.check_for_outdated_release(version, warnings_given_to_user)  # Store the computed URL
            openssl_urls[version] = openssl_url
            # Store the updated dictionary of URLS
            Openssl._openssl_url = openssl_urls
            # Store the updated dictionary of warnings
            Openssl._warnings_given = warnings_given_to_user

        return openssl_url

    def check_for_outdated_release(self, version, warnings_given_to_user):
        latest = 'ftp://ftp.openssl.org/source/openssl-{version}.tar.gz'
        older = 'http://www.openssl.org/source/old/{version_number}/openssl-{version_full}.tar.gz'
        # Try to use the url where the latest tarballs are stored. If the url does not exist (404), then
        # return the url for older format
        version_number = '.'.join([str(x) for x in version[:-1]])
        try:
            openssl_url = latest.format(version=version)
            urllib.urlopen(openssl_url)
        except IOError:
            openssl_url = older.format(version_number=version_number, version_full=version)
            # Checks if we already warned the user for this particular version of OpenSSL.
            # If not we display a warning message and mark this version
            if not warnings_given_to_user.get(version, False):
                tty.warn(
                    'This installation depends on an old version of OpenSSL, which may have known security issues. ')
                tty.warn('Consider updating to the latest version of this package.')
                tty.warn('More details at {homepage}'.format(homepage=Openssl.homepage))
                warnings_given_to_user[version] = True

        return openssl_url

    def install(self, spec, prefix):
        # OpenSSL uses a variable APPS in its Makefile. If it happens to be set
        # in the environment, then this will override what is set in the
        # Makefile, leading to build errors.
        env.pop('APPS', None)
        if spec.satisfies("arch=darwin-x86_64") or spec.satisfies("arch=ppc64"):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env['KERNEL_BITS'] = '64'
        config = Executable("./config")
        config("--prefix=%s" % prefix,
               "--openssldir=%s" % join_path(prefix, 'etc', 'openssl'),
               "zlib",
               "no-krb5",
               "shared")
        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r'-arch x86_64', '', 'Makefile')

        make()
        make("install")
