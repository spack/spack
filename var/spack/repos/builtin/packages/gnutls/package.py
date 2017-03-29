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
from spack import *


class Gnutls(AutotoolsPackage):
    """GnuTLS is a secure communications library implementing the SSL,
       TLS and DTLS protocols and technologies around them. It
       provides a simple C language application programming interface
       (API) to access the secure communications protocols as well as
       APIs to parse and write X.509, PKCS #12, OpenPGP and other
       required structures. It is aimed to be portable and efficient
       with focus on security and interoperability."""

    homepage = "http://www.gnutls.org"
    url      = "http://www.ring.gr.jp/pub/net/gnupg/gnutls/v3.3/gnutls-3.3.9.tar.xz"

    version('3.5.9', '0ab25eb6a1509345dd085bc21a387951')
    version('3.3.9', 'ff61b77e39d09f1140ab5a9cf52c58b6')

    # configure sez: Note that version 3.3.9 of gnutls doesn't support
    # nettle 3.0.
    depends_on("nettle@:2.9", when='@3.3.9')
    depends_on("nettle", when='@3.5:')
    depends_on("zlib", when='@3.5:')

    build_directory = 'spack-build'

    def configure_args(self):
        args = []
        if self.spec.satisfies('@3.5:'):
            # use shipped libraries, might be turned into variants
            args.append('--with-included-libtasn1')
            args.append('--with-included-unistring')
            args.append('--without-p11-kit')  # p11-kit@0.23.1: ...
        return args
