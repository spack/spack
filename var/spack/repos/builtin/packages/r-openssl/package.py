# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    homepage = "https://CRAN.R-project.org/package=openssl"
    url      = "https://cran.r-project.org/src/contrib/openssl_0.9.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/openssl"

    version('0.9.7', '86773824dce7d3d79abfef574ce2531a')
    version('0.9.6', '7ef137929d9dd07db690d35db242ba4b')
    version('0.9.4', '82a890e71ed0e74499878bedacfb8ccb')

    depends_on('openssl@1.0.1:')
