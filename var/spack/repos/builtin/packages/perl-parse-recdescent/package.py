# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlParseRecdescent(PerlPackage):
    """Generate Recursive-Descent Parsers"""

    homepage = "http://search.cpan.org/~jtbraun/Parse-RecDescent-1.967015/lib/Parse/RecDescent.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JT/JTBRAUN/Parse-RecDescent-1.967015.tar.gz"

    version('1.967015', '7a36d45d62a9b68603edcdbd276006cc')

    depends_on('perl-module-build', type='build')
