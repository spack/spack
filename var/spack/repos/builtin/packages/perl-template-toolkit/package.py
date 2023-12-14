# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2023 EMBL-European Bioinformatics Institute
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTemplateToolkit(PerlPackage):
    """Comprehensive template processing system"""

    homepage = "https://metacpan.org/pod/Template::Toolkit"
    url = "https://cpan.metacpan.org/authors/id/A/AB/ABW/Template-Toolkit-3.101.tar.gz"

    maintainers("EbiArnie")

    version("3.101", sha256="d2a32dd6c21e4b37c6a93df8087ca9e880cfae613a3e5efaea307b0bdcaedb58")

    def configure_args(self):
        return [
            'TT_XS_DEFAULT=y',
            'TT_ACCEPT=y'
        ]

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Template::Toolkit; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
