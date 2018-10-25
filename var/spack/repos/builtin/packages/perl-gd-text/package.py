# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGdText(PerlPackage):
    """Text utilities for use with GD"""

    homepage = "http://search.cpan.org/~mverb/GDTextUtil-0.86/Text.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MV/MVERB/GDTextUtil-0.86.tar.gz"

    version('0.86', '941ad06eadc86b47f3a32da405665c41')

    depends_on('perl-gd', type=('build', 'run'))
