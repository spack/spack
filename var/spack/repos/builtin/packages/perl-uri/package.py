# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlUri(PerlPackage):
    """Uniform Resource Identifiers (absolute and relative)"""

    homepage = "http://search.cpan.org/~ether/URI-1.72/lib/URI.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/URI-1.72.tar.gz"

    version('1.72', 'cd56d81ed429efaa97e7f3ff08851b48')

    depends_on('perl-test-needs', type=('build', 'run'))
