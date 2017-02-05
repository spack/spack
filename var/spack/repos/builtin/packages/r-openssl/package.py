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


class ROpenssl(RPackage):
    """Bindings to OpenSSL libssl and libcrypto, plus custom SSH pubkey
    parsers. Supports RSA, DSA and EC curves P-256, P-384 and P-521.
    Cryptographic signatures can either be created and verified manually or via
    x509 certificates. AES can be used in cbc, ctr or gcm mode for symmetric
    encryption; RSA for asymmetric (public key) encryption or EC for Diffie
    Hellman. High-level envelope functions combine RSA and AES for encrypting
    arbitrary sized data. Other utilities include key generators, hash
    functions (md5, sha1, sha256, etc), base64 encoder, a secure random number
    generator, and 'bignum' math methods for manually performing crypto
    calculations on large multibyte integers."""

    homepage = "https://github.com/jeroenooms/openssl#readme"
    url      = "https://cran.r-project.org/src/contrib/openssl_0.9.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/openssl"

    version('0.9.6', '7ef137929d9dd07db690d35db242ba4b')
    version('0.9.4', '82a890e71ed0e74499878bedacfb8ccb')

    depends_on('openssl@1.0.1:')
