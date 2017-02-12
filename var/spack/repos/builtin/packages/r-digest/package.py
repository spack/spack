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


class RDigest(RPackage):
    """Implementation of a function 'digest()' for the creation of hash digests
    of arbitrary R objects (using the md5, sha-1, sha-256, crc32, xxhash and
    murmurhash algorithms) permitting easy comparison of R language objects, as
    well as a function 'hmac()' to create hash-based message authentication
    code. The md5 algorithm by Ron Rivest is specified in RFC 1321, the sha-1
    and sha-256 algorithms are specified in FIPS-180-1 and FIPS-180-2, and the
    crc32 algorithm is described in
    ftp://ftp.rocksoft.com/cliens/rocksoft/papers/crc_v3.txt. For md5, sha-1,
    sha-256 and aes, this package uses small standalone implementations that
    were provided by Christophe Devine. For crc32, code from the zlib library
    is used. For sha-512, an implementation by Aaron D. Gifford is used. For
    xxhash, the implementation by Yann Collet is used. For murmurhash, an
    implementation by Shane Day is used. Please note that this package is not
    meant to be deployed for cryptographic purposes for which more
    comprehensive (and widely tested) libraries such as OpenSSL should be
    used."""

    homepage = "http://dirk.eddelbuettel.com/code/digest.html"
    url      = "https://cran.r-project.org/src/contrib/digest_0.6.12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/digest"

    version('0.6.12', '738efd4d9a37c5a4001ae66e954ce07e')
    version('0.6.11', '52a864f55846b48b3cab0b5d0304a82a')
    version('0.6.9',  '48048ce6c466bdb124716e45ba4a0e83')

    depends_on('r@2.4.1:')
