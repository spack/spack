# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFontTtf(PerlPackage):
    """Perl module for TrueType Font hacking"""

    homepage = "http://search.cpan.org/~bhallissy/Font-TTF-1.06/lib/Font/TTF.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BH/BHALLISSY/Font-TTF-1.06.tar.gz"

    version('1.06', '241b59310ad4450e6e050d5e790f1b21')
