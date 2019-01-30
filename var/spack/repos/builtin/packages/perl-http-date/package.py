# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpDate(PerlPackage):
    """Date conversion routines"""

    homepage = "http://search.cpan.org/~gaas/HTTP-Date-6.02/lib/HTTP/Date.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Date-6.02.tar.gz"

    version('6.02', '52b7a0d5982d61be1edb217751d7daba')
