# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParseRecdescent(PerlPackage):
    """Generate Recursive-Descent Parsers"""

    homepage = "https://metacpan.org/pod/Parse::RecDescent"
    url = "https://cpan.metacpan.org/authors/id/J/JT/JTBRAUN/Parse-RecDescent-1.967015.tar.gz"

    version(
        "1.967.015",
        sha256="1943336a4cb54f1788a733f0827c0c55db4310d5eae15e542639c9dd85656e37",
        url="https://cpan.metacpan.org/authors/id/J/JT/JTBRAUN/Parse-RecDescent-1.967015.tar.gz",
    )
    version(
        "1.967.014",
        sha256="7041c483431fefd08eb66944fb5f8f7fb0fc595c08b33ed2f4c7037b8acccdcd",
        url="https://cpan.metacpan.org/authors/id/J/JT/JTBRAUN/Parse-RecDescent-1.967014.tar.gz",
    )

    depends_on("perl-module-build", type="build")
