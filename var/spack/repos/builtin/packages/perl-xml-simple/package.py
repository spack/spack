# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PerlXmlSimple(PerlPackage):
    """An API for simple XML files"""

    homepage = "https://metacpan.org/pod/XML::Simple"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-Simple-2.24.tar.gz"

    version('2.24', sha256='9a14819fd17c75fbb90adcec0446ceab356cab0ccaff870f2e1659205dc2424f')

    depends_on('perl-xml-parser', type=('build', 'run'))
