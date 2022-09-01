# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestNeeds(PerlPackage):
    """Skip tests when modules not available."""

    homepage = "https://metacpan.org/pod/Test::Needs"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-0.002009.tar.gz"

    version("0.002.009", sha256="571c21193ad16195df58b06b268798796a391b398c443271721d2cc0fb7c4ac3",
            url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-0.002009.tar.gz")
    version("0.002_008", sha256="d9b275ff73fc10d78aa4fc3bc19fd5fa624a4c7410cb062d763fc50905b112c7")
    version("0.002_007", sha256="c077e122afa54f39f56055d5847fd02b0d615cb70d76df7716ccfd43b59c556d")
    version("0.002.006", sha256="77f9fff0c96c5e09f34d0416b3533c3319f7cd0bb1f7fe8f8072ad59f433f0e5",
            url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-0.002006.tar.gz")
    version("0.002.005", sha256="5a4f33983586edacdbe00a3b429a9834190140190dab28d0f873c394eb7df399",
            url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-0.002005.tar.gz")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
