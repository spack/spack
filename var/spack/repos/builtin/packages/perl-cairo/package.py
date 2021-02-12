# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCairo(PerlPackage):
    """Perl interface to the cairo 2d vector graphics library"""

    homepage = "http://search.cpan.org/~xaoc/Cairo/lib/Cairo.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/Cairo-1.106.tar.gz"

    version('1.109', sha256='8219736e401c2311da5f515775de43fd87e6384b504da36a192f2b217643077f')
    version('1.108', sha256='6042cb7dc51675ab23437059c6384713c5fbbce844c4c60017d2e061948f05da')
    version('1.107', sha256='5e1de126ddf93bd5b13f13a52f50d7f7af1157265b7f10e53d585ee1827be169')
    version('1.106', sha256='e64803018bc7cba49e73e258547f5378cc4249797beafec524852140f49c45c4')

    depends_on('cairo')
    depends_on('perl-extutils-depends')
    depends_on('perl-extutils-pkgconfig')
