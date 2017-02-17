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
import llnl.util.tty as tty

from spack import *


class Openssl(Package):
    """OpenSSL is an open source project that provides a robust,
       commercial-grade, and full-featured toolkit for the Transport
       Layer Security (TLS) and Secure Sockets Layer (SSL) protocols.
       It is also a general-purpose cryptography library."""
    homepage = "http://www.openssl.org"
    url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"
    list_url = "https://www.openssl.org/source/old/"
    list_depth = 2

    # Note: Version 1.0.2 is the "long-term support" version that will
    # remain supported until 2019. We could thus make this version the
    # preferred version, if we find that many packages cannot handle
    # version 1.1.
    version('1.1.0e', '51c42d152122e474754aea96f66928c6')
    version('1.1.0d', '711ce3cd5f53a99c0e12a7d5804f0f63')
    version('1.1.0c', '601e8191f72b18192a937ecf1a800f3f')
    version('1.0.2k', 'f965fc0bf01bf882b31314b61391ae65')
    version('1.0.2j', '96322138f0b69e61b7212bc53d5e912b')
    version('1.0.2i', '678374e63f8df456a697d3e5e5a931fb')
    version('1.0.2h', '9392e65072ce4b614c1392eefc1f23d0')
    version('1.0.2g', 'f3c710c045cdee5fd114feb69feba7aa')
    version('1.0.2f', 'b3bf73f507172be9292ea2a8c28b659d')
    version('1.0.2e', '5262bfa25b60ed9de9f28d5d52d77fc5')
    version('1.0.2d', '38dd619b2e77cbac69b99f52a053d25a')
    version('1.0.1u', '130bb19745db2a5a09f22ccbbf7e69d0')
    version('1.0.1t', '9837746fcf8a6727d46d22ca35953da1')
    version('1.0.1r', '1abd905e079542ccae948af37e393d28')
    version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')

    depends_on('zlib')

    # 'make test' requires Test::More version 0.96
    depends_on('perl@5.14.0:', type='build')

    parallel = False

    def handle_fetch_error(self, error):
        tty.warn("Fetching OpenSSL failed. This may indicate that OpenSSL has "
                 "been updated, and the version in your instance of Spack is "
                 "insecure. Consider updating to the latest OpenSSL version.")

    def install(self, spec, prefix):
        # OpenSSL uses a variable APPS in its Makefile. If it happens to be set
        # in the environment, then this will override what is set in the
        # Makefile, leading to build errors.
        env.pop('APPS', None)

        if spec.satisfies('target=x86_64') or spec.satisfies('target=ppc64'):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env['KERNEL_BITS'] = '64'

        options = ['zlib', 'shared']
        if spec.satisfies('@1.0'):
            options.append('no-krb5')

        config = Executable('./config')
        config('--prefix=%s' % prefix,
               '--openssldir=%s' % join_path(prefix, 'etc', 'openssl'),
               *options)

        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r'-arch x86_64', '', 'Makefile')

        make()
        if self.run_tests:
            make('test')            # 'VERBOSE=1'
        make('install')
