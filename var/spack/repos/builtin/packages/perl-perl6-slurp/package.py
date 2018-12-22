# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPerl6Slurp(PerlPackage):
    """Perl6::Slurp - Implements the Perl 6 'slurp' built-in"""

    homepage = "http://search.cpan.org/~dconway/Perl6-Slurp-0.051005/lib/Perl6/Slurp.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/Perl6-Slurp-0.051005.tar.gz"

    version('0.051005', '6095c8df495c7983f36996ed78c5ead7')

    depends_on('perl@5.8:5.999', type=('build', 'run'))
