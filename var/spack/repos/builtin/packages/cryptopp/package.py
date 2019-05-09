# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('6.1.0', sha256='21289d2511101a9350c87c8eb1f4982d4a266e8037b19dab79a32cc13ea108c7')
    version('6.0.0', sha256='64ac2db96b3f1b7a23675e2be95d16c96055edffa2d5e2de6245fdb6baa92dda')
    version('5.6.5', sha256='a75ef486fe3128008bbb201efee3dcdcffbe791120952910883b26337ec32c34')
    version('5.6.4', sha256='be430377b05c15971d5ccb6e44b4d95470f561024ed6d701fe3da3a188c84ad7')
    version('5.6.3', '3c5b70e2ec98b7a24988734446242d07')
    version('5.6.2', '7ed022585698df48e65ce9218f6c6a67')
    version('5.6.1', '96cbeba0907562b077e26bcffb483828')

    depends_on('gmake', type='build')

    def url_for_version(self, version):
        url = '{0}/{1}{2}.zip'
        return url.format(self.homepage, self.name, version.joined)

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
