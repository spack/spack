# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlXmlParserLite(PerlPackage):
    """Lightweight pure-perl XML Parser (based on regexps)"""

    homepage = "http://search.cpan.org/~phred/XML-Parser-Lite-0.721/lib/XML/Parser/Lite.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/XML-Parser-Lite-0.721.tar.gz"

    version('0.721', 'ad8a87b9bf413aa540c7cb724d650808')

    depends_on('perl-test-requires', type=('build', 'run'))
