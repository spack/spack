# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpCookies(PerlPackage):
    """HTTP cookie jars"""

    homepage = "http://search.cpan.org/~oalders/HTTP-Cookies-6.04/lib/HTTP/Cookies.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Cookies-6.04.tar.gz"

    version('6.04', '7bf1e277bd5c886bc18d21eb8423b65f')

    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
