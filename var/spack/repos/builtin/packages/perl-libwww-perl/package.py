# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLibwwwPerl(PerlPackage):
    """The libwww-perl collection is a set of Perl modules which provides
    a simple and consistent application programming interface to the
    World-Wide Web. The main focus of the library is to provide classes and
    functions that allow you to write WWW clients."""

    homepage = "https://github.com/libwww-perl/libwww-perl"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-6.33.tar.gz"

    version('6.33', '2e15c1c789ac9036c99d094e47e3da23')

    depends_on('perl-encode-locale', type=('build', 'run'))
    depends_on('perl-file-listing', type=('build', 'run'))
    depends_on('perl-html-parser', type=('build', 'run'))
    depends_on('perl-http-cookies', type=('build', 'run'))
    depends_on('perl-http-daemon', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-http-negotiate', type=('build', 'run'))
    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-net-http', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-www-robotrules', type=('build', 'run'))
