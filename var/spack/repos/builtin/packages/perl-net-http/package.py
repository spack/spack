# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlNetHttp(PerlPackage):
    """Low-level HTTP connection (client)"""

    homepage = "http://search.cpan.org/~oalders/Net-HTTP-6.17/lib/Net/HTTP.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/Net-HTTP-6.17.tar.gz"

    version('6.17', '068fa02fd3c8a5b63316025b5a24844c')

    depends_on('perl-uri', type=('build', 'run'))
