# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2023 EMBL-European Bioinformatics Institute
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTermTable(PerlPackage):
    """Format a header and rows into a table"""

    homepage = "https://metacpan.org/pod/Term::Table"
    url = "https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Term-Table-0.018.tar.gz"

    maintainers("EbiArnie")

    version("0.018", sha256="9159b9131ee6b3f3956b74f45422985553574babbfaeba60be5c17bc114ac011")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Term::Table; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
