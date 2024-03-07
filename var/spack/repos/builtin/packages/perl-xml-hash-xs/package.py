# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlHashXs(PerlPackage):
    """Simple and fast hash to XML and XML to hash conversion written in C"""

    homepage = "https://metacpan.org/pod/XML::Hash::XS"
    url = "https://cpan.metacpan.org/authors/id/Y/YO/YOREEK/XML-Hash-XS-0.56.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.56", sha256="be4c60ded94c5ebe53a81ef74928dfbec9613986d2a6056dd253665c6ae9802f")

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use XML::Hash::XS; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
