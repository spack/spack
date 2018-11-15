# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHtmlParser(PerlPackage):
    """HTML parser class"""

    homepage = "http://search.cpan.org/~gaas/HTML-Parser-3.72/Parser.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTML-Parser-3.72.tar.gz"

    version('3.72', 'eb7505e5f626913350df9dd4a03d54a8')

    depends_on('perl-html-tagset', type=('build', 'run'))
