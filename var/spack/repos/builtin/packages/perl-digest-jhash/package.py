# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestJhash(PerlPackage):
    """Perl extension for 32 bit Jenkins Hashing Algorithm"""

    homepage = "https://metacpan.org/pod/Digest::JHash"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Digest-JHash-0.10.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.10", sha256="c746cf0a861a004090263cd54d7728d0c7595a0cf90cbbfd8409b396ee3b0063")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Digest::JHash; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
