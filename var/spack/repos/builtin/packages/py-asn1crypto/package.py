# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyAsn1crypto(PythonPackage):
    """Python ASN.1 library with a focus on performance and a pythonic API """

    homepage = "https://github.com/wbond/asn1crypto"
    pypi = "asn1crypto/asn1crypto-0.22.0.tar.gz"

    version('1.4.0', sha256='f4f6e119474e58e04a2b1af817eb585b4fd72bdd89b998624712b5c99be7641c')
    version('1.3.0', sha256='5a215cb8dc12f892244e3a113fe05397ee23c5c4ca7a69cd6e69811755efc42d')
    version('1.2.0', sha256='87620880a477123e01177a1f73d0f327210b43a3cdbd714efcd2fa49a8d7b384')
    version('1.1.0', sha256='5abe83e773026162e4869f4ac16edf7554f661e8cc0bb6d2be3bc6915456731b')
    version('1.0.1', sha256='0b199f211ae690df3db4fd6c1c4ff976497fb1da689193e368eedbadc53d9292')
    version('1.0.0', sha256='f822954b90c4c44f002e2cd46d636ab630f1fe4df22c816a82b66505c404eb2a')
    version('0.24.0', sha256='9d5c20441baf0cb60a4ac34cc447c6c189024b6b4c6cd7877034f4965c464e49')
    version('0.22.0', sha256='cbbadd640d3165ab24b06ef25d1dca09a3441611ac15f6a6b452474fdf0aed1a')

    depends_on('py-setuptools', type='build')
