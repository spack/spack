# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlClassInspector(PerlPackage):
    """Get information about a class and its structure"""

    homepage = "http://search.cpan.org/~plicease/Class-Inspector-1.32/lib/Class/Inspector.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PL/PLICEASE/Class-Inspector-1.32.tar.gz"

    version('1.32', 'db471d6ecf47fa054726553319b7c34f')
