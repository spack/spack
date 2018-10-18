# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cryptopp(MakefilePackage):
    """Crypto++ is an open-source C++ library of cryptographic schemes. The
    library supports a number of different cryptography algorithms, including
    authenticated encryption schemes (GCM, CCM), hash functions (SHA-1, SHA2),
    public-key encryption (RSA, DSA), and a few obsolete/historical encryption
    algorithms (MD5, Panama)."""

    homepage = "http://www.cryptopp.com"
    url      = "http://www.cryptopp.com/cryptopp700.zip"

    version('7.0.0', '8f34884b572901b6ede89bd18f1c7ef6')
    version('5.6.3', '3c5b70e2ec98b7a24988734446242d07')
    version('5.6.2', '7ed022585698df48e65ce9218f6c6a67')
    version('5.6.1', '96cbeba0907562b077e26bcffb483828')

    depends_on('gmake', type='build')

    def url_for_version(self, version):
        url = '{0}/{1}{2}.zip'
        return url.format(self.homepage, self.name, version.joined)

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
