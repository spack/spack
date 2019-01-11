# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLwp(PerlPackage):
    """The World-Wide Web library for Perl"""

    homepage = "http://search.cpan.org/~oalders/libwww-perl-6.29/lib/LWP.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-6.29.tar.gz"

    version('6.29', 'efec8d563ffd3652333356aa722c2b56')

    depends_on('perl-test-requiresinternet', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-file-listing', type=('build', 'run'))
    depends_on('perl-http-daemon', type=('build', 'run'))
    depends_on('perl-html-parser', type=('build', 'run'))
    depends_on('perl-http-cookies', type=('build', 'run'))
    depends_on('perl-www-robotrules', type=('build', 'run'))
    depends_on('perl-test-fatal', type=('build', 'run'))
    depends_on('perl-http-negotiate', type=('build', 'run'))
    depends_on('perl-net-http', type=('build', 'run'))
