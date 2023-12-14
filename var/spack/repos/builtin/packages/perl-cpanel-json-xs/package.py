# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2023 EMBL-European Bioinformatics Institute
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCpanelJsonXs(PerlPackage):
    """CPanel fork of JSON::XS, fast and correct serializing"""

    homepage = "https://metacpan.org/pod/Cpanel::JSON::XS"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Cpanel-JSON-XS-4.37.tar.gz"

    maintainers("EbiArnie")

    version("4.37", sha256="c241615a0e17ff745aaa86bbf466a6e29cd240515e65f06a7a05017b619e6d4b")

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Cpanel::JSON::XS; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
