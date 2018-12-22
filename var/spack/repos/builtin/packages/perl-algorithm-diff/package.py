# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlAlgorithmDiff(PerlPackage):
    """Compute 'intelligent' differences between two files / lists"""

    homepage = "http://search.cpan.org/~tyemq/Algorithm-Diff-1.1903/lib/Algorithm/Diff.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TY/TYEMQ/Algorithm-Diff-1.1903.tar.gz"

    version('1.1903', '0e8add21a641b8d66436df0c2024bf3b')
