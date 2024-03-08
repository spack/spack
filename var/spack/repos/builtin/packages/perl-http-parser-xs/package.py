# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpParserXs(PerlPackage):
    """A fast, primitive HTTP request parser"""

    homepage = "https://metacpan.org/pod/HTTP::Parser::XS"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZUHO/HTTP-Parser-XS-0.17.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.17", sha256="794e6833e326b10d24369f9cdbfc1667105ef6591e8f41e561a3d41a7027a809")

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use HTTP::Parser::XS; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
