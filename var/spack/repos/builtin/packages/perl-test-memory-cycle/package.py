# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestMemoryCycle(PerlPackage):
    """Check for memory leaks and circular memory references"""

    homepage = "http://search.cpan.org/~petdance/Test-Memory-Cycle-1.06/Cycle.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/Test-Memory-Cycle-1.06.tar.gz"

    version('1.06', '397e709ba33d3883b5fb2bc49e3a70b0')

    depends_on('perl-padwalker', type=('build', 'run'))
    depends_on('perl-devel-cycle', type=('build', 'run'))
