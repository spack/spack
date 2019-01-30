# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestFatal(PerlPackage):
    """Incredibly simple helpers for testing code with exceptions"""

    homepage = "http://search.cpan.org/~rjbs/Test-Fatal-0.014/lib/Test/Fatal.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Fatal-0.014.tar.gz"

    version('0.014', '7954f6d2e3607be10c0fbd69063a3d1b')

    depends_on('perl-try-tiny', type=('build', 'run'))
