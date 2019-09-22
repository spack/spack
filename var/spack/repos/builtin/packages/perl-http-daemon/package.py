# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpDaemon(PerlPackage):
    """A simple http server class"""

    homepage = "http://search.cpan.org/~gaas/HTTP-Daemon-6.01/lib/HTTP/Daemon.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Daemon-6.01.tar.gz"

    version('6.01', 'ed0ae02d25d7f1e89456d4d69732adc2')

    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
    depends_on('perl-module-build-tiny', type='build')
