# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlBitVector(PerlPackage):
    """Efficient bit vector, set of integers and "big int" math library"""

    homepage = "http://search.cpan.org/~stbey/Bit-Vector-7.4/Vector.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/S/ST/STBEY/Bit-Vector-7.4.tar.gz"

    version('7.4', 'bf67f144e5be5327ed79d4c69e6e0086')

    depends_on('perl-carp-clan', type=('build', 'run'))
