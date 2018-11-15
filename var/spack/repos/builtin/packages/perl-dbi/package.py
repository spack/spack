# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDbi(PerlPackage):
    """The DBI is the standard database interface module for Perl. It defines
    a set of methods, variables and conventions that provide a consistent
    database interface independent of the actual database being used."""

    homepage = "https://dbi.perl.org/"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TI/TIMB/DBI-1.636.tar.gz"

    version('1.636',  '60f291e5f015550dde71d1858dfe93ba')
