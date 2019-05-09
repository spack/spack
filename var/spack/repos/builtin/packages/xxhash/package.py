# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xxhash(MakefilePackage):
    """xxHash is an Extremely fast Hash algorithm, running at RAM speed
    limits. It successfully completes the SMHasher test suite which
    evaluates collision, dispersion and randomness qualities of hash
    functions. Code is highly portable, and hashes are identical on all
    platforms (little / big endian).
    """

    homepage = "https://github.com/Cyan4973/xxHash"
    url      = "https://github.com/Cyan4973/xxHash/archive/v0.6.5.tar.gz"

    version('0.6.5', '6af3a964f3c2accebce66e54b44b6446')
    version('0.6.4', '3c071c95e31bd601cca149cc354e6f19')
    version('0.6.3', 'f2ec1497317c0eb89addd7f333c83228')
    version('0.6.2', 'b2d12d99094b824e0a5f3ab63abc6c58')
    version('0.6.1', 'f4ced3767aad8384b1ecb73bd5f992ca')
    version('0.6.0', 'e0fd163b07ab0038f389a180dc263cf2')
    version('0.5.1', '9417fd8a4d88204b680e21a60f0ccada')
    version('0.5.0', '42e9a31a2cfc2f626fde17e84a0b6bb7')

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter('/usr/local', prefix)
