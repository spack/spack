# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlXmlSimple(PerlPackage):
    """An API for simple XML files"""

    homepage = "http://search.cpan.org/~grantm/XML-Simple/lib/XML/Simple.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-Simple-2.24.tar.gz"

    version('2.24', '1cd2e8e3421160c42277523d5b2f4dd2')

    depends_on('perl-xml-parser', type=('build', 'run'))
