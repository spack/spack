# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMathCephes(PerlPackage):
    """This module provides an interface to over 150 functions of the
       cephes math library of Stephen Moshier."""

    homepage = "http://search.cpan.org/~shlomif/Math-Cephes/lib/Math/Cephes.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Math-Cephes-0.5305.tar.gz"

    version('0.5305', '30922dd213783aaaf91a47626f6a1853')
