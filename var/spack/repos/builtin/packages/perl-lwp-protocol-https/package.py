# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLwpProtocolHttps(PerlPackage):
    """ Provide https support for LWP::UserAgent"""

    homepage = "http://search.cpan.org/~gaas/LWP-Protocol-https-6.04/lib/LWP/Protocol/https.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/LWP-Protocol-https-6.04.tar.gz"

    version('6.04', '1b422a7d3b5fed1eb4d748fdc9fd79a4')

    depends_on('perl-test-requiresinternet', type=('build', 'run'))
    depends_on('perl-io-socket-ssl', type=('build', 'run'))
    depends_on('perl-net-http', type=('build', 'run'))
    depends_on('perl-mozilla-ca', type=('build', 'run'))
    depends_on('perl-lwp', type=('build', 'run'))
