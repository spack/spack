# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCairo(PerlPackage):
    """Perl interface to the cairo 2d vector graphics library"""

    homepage = "http://search.cpan.org/~xaoc/Cairo/lib/Cairo.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/Cairo-1.106.tar.gz"

    version('1.106', '47ca0ae0f5b9bc4c16a27627ff48bd8b')

    depends_on('cairo')
    depends_on('perl-extutils-depends')
    depends_on('perl-extutils-pkgconfig')
