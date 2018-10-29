# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestException(PerlPackage):
    """Test exception-based code"""

    homepage = "http://search.cpan.org/~exodist/Test-Exception-0.43/lib/Test/Exception.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/EX/EXODIST/Test-Exception-0.43.tar.gz"

    version('0.43', '572d355026fb0b87fc2b8c64b83cada0')

    depends_on('perl-sub-uplevel', type=('build', 'run'))
