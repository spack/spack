# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlEncodeLocale(PerlPackage):
    """Determine the locale encoding"""

    homepage = "http://search.cpan.org/~gaas/Encode-Locale-1.05/lib/Encode/Locale.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Encode-Locale-1.05.tar.gz"

    version('1.05', 'fcfdb8e4ee34bcf62aed429b4a23db27')
