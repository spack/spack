# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDevelCycle(PerlPackage):
    """Find memory cycles in objects"""

    homepage = "http://search.cpan.org/~lds/Devel-Cycle-1.12/lib/Devel/Cycle.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LD/LDS/Devel-Cycle-1.12.tar.gz"

    version('1.12', '3d9a963da87b17398fab9acbef63f277')
