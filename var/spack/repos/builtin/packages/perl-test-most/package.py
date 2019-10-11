# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestMost(PerlPackage):
    """Most commonly needed test functions and features."""

    homepage = "http://search.cpan.org/~ovid/Test-Most-0.35/lib/Test/Most.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OV/OVID/Test-Most-0.35.tar.gz"

    version('0.35', '03dbabd34d6f40af8bd47f5fbb0c6989')

    depends_on('perl-exception-class', type=('build', 'run'))
    depends_on('perl-test-differences', type=('build', 'run'))
    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-warn', type=('build', 'run'))
    depends_on('perl-test-deep', type=('build', 'run'))
