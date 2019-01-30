# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileListing(PerlPackage):
    """Parse directory listing"""

    homepage = "http://search.cpan.org/~gaas/File-Listing-6.04/lib/File/Listing.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/File-Listing-6.04.tar.gz"

    version('6.04', '83f636b477741f3a014585bb9cc079a6')

    depends_on('perl-http-date', type=('build', 'run'))
