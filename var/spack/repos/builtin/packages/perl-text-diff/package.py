# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextDiff(PerlPackage):
    """Provides a basic set of services akin to the GNU diff utility."""

    homepage = "http://search.cpan.org/~neilb/Text-Diff-1.45/lib/Text/Diff.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Text-Diff-1.45.tar.gz"

    version('1.45', 'edf57b6189f7651a6be454062a4e6d9c')

    depends_on('perl-algorithm-diff', type=('build', 'run'))
