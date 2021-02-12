# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextCsv(PerlPackage):
    """Comma-separated values manipulator (using XS or PurePerl)"""

    homepage = "http://search.cpan.org/~ishigaki/Text-CSV/lib/Text/CSV.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IS/ISHIGAKI/Text-CSV-1.95.tar.gz"

    version('2.00', sha256='8ccbd9195805222d995844114d0e595bb24ce188f85284dbf256080311cbb2c2')
    version('1.99', sha256='e74ec039b12cc51d346bf1d814af7db8a05cb0a98340e7547a21646da8668cd2')
    version('1.98', sha256='dafc7d0ab30776224ac69d5d41680f1296b936116909c5e4de9a5d2973746402')
    version('1.97', sha256='cc350462efa8d39d5c8a1da5f205bc31620cd52d9865a769c8e3ed1b41640fd5')
    version('1.96', sha256='6957c9175cc8b80e36255e154831ad5c77b7b0b3a606dd554fcf2cb2caf1a52b')
    version('1.95', sha256='7e0a11d9c1129a55b68a26aa4b37c894279df255aa63ec8341d514ab848dbf61')
