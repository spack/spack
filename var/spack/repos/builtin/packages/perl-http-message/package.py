# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpMessage(PerlPackage):
    """HTTP style message (base class)"""

    homepage = "http://search.cpan.org/~oalders/HTTP-Message-6.13/lib/HTTP/Status.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Message-6.13.tar.gz"

    version('6.13', '4c1b7c6ee114c1cff69379ec9651d9ac')

    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-encode-locale', type=('build', 'run'))
    depends_on('perl-io-html', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
