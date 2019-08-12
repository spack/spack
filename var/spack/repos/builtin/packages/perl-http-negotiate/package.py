# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpNegotiate(PerlPackage):
    """Choose a variant to serve"""

    homepage = "http://search.cpan.org/~gaas/HTTP-Negotiate-6.01/lib/HTTP/Negotiate.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Negotiate-6.01.tar.gz"

    version('6.01', '1236195250e264d7436e7bb02031671b')

    depends_on('perl-http-message', type=('build', 'run'))
