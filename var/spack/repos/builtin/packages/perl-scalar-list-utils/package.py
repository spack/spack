# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlScalarListUtils(PerlPackage):
    """Scalar::Util - A selection of general-utility scalar subroutines"""

    homepage = "https://metacpan.org/pod/Scalar::Util"
    url      = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-1.50.tar.gz"

    version('1.55',     sha256='4d2bdc1c72a7bc4d69d6a5cc85bc7566497c3b183c6175b832784329d58feb4b')
    version('1.54',     sha256='a6eda0eb8fd69890c2369ad12c1fd1b8aab5b38793cac3688d7fc402c630bf79')
    version('1.53',     sha256='bd4086b066fb3b18a0be2e7d9bc100a99aa0f233ad659492340415c7b2bdae99')
    version('1.52_001', sha256='2cdcbd0d3fb7ba98a0c59fb4dca77bc74370a072a0857776ba2396cc4f765123')
    version('1.52',     sha256='279d78cef84acae280da4dfb95eff0c9865d1611b1a3b026baddf42d1ba01de4')
    version('1.51',     sha256='d9c8eab1ac5a6fc75a7e836304626e2cb7b13cf8c9b10d491a144e1ef6760a76')
    version('1.50', sha256='06aab9c693380190e53be09be7daed20c5d6278f71956989c24cca7782013675')
