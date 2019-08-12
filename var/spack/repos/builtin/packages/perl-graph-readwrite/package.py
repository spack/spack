# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGraphReadwrite(PerlPackage):
    """Write out directed graph in Dot format"""

    homepage = "http://search.cpan.org/~neilb/Graph-ReadWrite/lib/Graph/Writer/Dot.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Graph-ReadWrite-2.09.tar.gz"

    version('2.09', '5cd9191eadd2fe8fe8bb431575434f67')
