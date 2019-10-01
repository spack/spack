# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgcrypt(AutotoolsPackage):
    """Libgcrypt is a general purpose cryptographic library based on
       the code from GnuPG. It provides functions for all cryptographic
       building blocks: symmetric ciphers, hash algorithms, MACs, public
       key algorithms, large integer functions, random numbers and a lot
       of supporting functions. """
    homepage = "http://www.gnu.org/software/libgcrypt/"
    url = "https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-1.8.1.tar.bz2"

    version('1.8.4', sha256='f638143a0672628fde0cad745e9b14deb85dffb175709cacc1f4fe24b93f2227')
    version('1.8.1', 'b21817f9d850064d2177285f1073ec55')
    version('1.7.6', '54e180679a7ae4d090f8689ca32b654c')
    version('1.6.2', 'b54395a93cb1e57619943c082da09d5f')

    depends_on("libgpg-error")
