# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2023 EMBL-European Bioinformatics Institute
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModulePluggable(PerlPackage):
    """Automatically give your module the ability to have plugins"""

    homepage = "https://metacpan.org/pod/Module::Pluggable"
    url = "https://cpan.metacpan.org/authors/id/S/SI/SIMONW/Module-Pluggable-5.2.tar.gz"

    maintainers("EbiArnie")

    version("5.2", sha256="b3f2ad45e4fd10b3fb90d912d78d8b795ab295480db56dc64e86b9fa75c5a6df")

    depends_on("perl@5.5.30:", type=("build", "link", "run", "test"))

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Module::Pluggable; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
