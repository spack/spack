# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgcrypt(AutotoolsPackage):
    """Libgcrypt is a general purpose cryptographic library based on
    the code from GnuPG. It provides functions for all cryptographic
    building blocks: symmetric ciphers, hash algorithms, MACs, public
    key algorithms, large integer functions, random numbers and a lot
    of supporting functions."""

    homepage = "http://www.gnu.org/software/libgcrypt/"
    url = "https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-1.8.5.tar.bz2"

    version('1.8.5', sha256='3b4a2a94cb637eff5bdebbcaf46f4d95c4f25206f459809339cdada0eb577ac3')
    version('1.8.4', sha256='f638143a0672628fde0cad745e9b14deb85dffb175709cacc1f4fe24b93f2227')
    version('1.8.1', sha256='7a2875f8b1ae0301732e878c0cca2c9664ff09ef71408f085c50e332656a78b3')
    version('1.7.6', sha256='626aafee84af9d2ce253d2c143dc1c0902dda045780cc241f39970fc60be05bc')
    version('1.6.2', sha256='de084492a6b38cdb27b67eaf749ceba76bf7029f63a9c0c3c1b05c88c9885c4c')

    depends_on('libgpg-error@1.25:')
