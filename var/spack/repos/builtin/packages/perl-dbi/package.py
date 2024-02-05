# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbi(PerlPackage):
    """The DBI is the standard database interface module for Perl. It defines
    a set of methods, variables and conventions that provide a consistent
    database interface independent of the actual database being used."""

    homepage = "https://dbi.perl.org/"
    url = "http://search.cpan.org/CPAN/authors/id/T/TI/TIMB/DBI-1.636.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.643", sha256="8a2b993db560a2c373c174ee976a51027dd780ec766ae17620c20393d2e836fa")
    version("1.636", sha256="8f7ddce97c04b4b7a000e65e5d05f679c964d62c8b02c94c1a7d815bb2dd676c")
