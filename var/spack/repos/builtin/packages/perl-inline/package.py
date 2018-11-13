# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlInline(PerlPackage):
    """Write Perl Subroutines in Other Programming Languages"""

    homepage = "http://search.cpan.org/~ingy/Inline-0.80/lib/Inline.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Inline-0.80.tar.gz"

    version('0.80', '510bbac46e727bcaf240b7feac2646c9')

    depends_on('perl-test-warn', type=('build', 'run'))
