# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubQuote(PerlPackage):
    """Efficient generation of subroutines via string eval."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/H/HA/HAARG"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-2.006006.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.006_007", sha256="ccb226d1d1a0d1cde99eabe98cb4eeb89f9f9eaf961be226d903e9ac333e5220")
    version(
        "2.006.006",
        sha256="6e4e2af42388fa6d2609e0e82417de7cc6be47223f576592c656c73c7524d89d",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-2.006006.tar.gz",
    )
    version("2.006_005", sha256="375e007ba99b3bad5d40aef8bbec6398fb40911b399b8909439fc0135535f444")
    version("2.006_004", sha256="52317dbede6812c92696e11af88026a148948875e48d58bfd4e4a3bb38f2397e")
    version(
        "2.006.003",
        sha256="be1f3a6f773f351f203cdc8f614803ac492b77d15fd68d5b1f0cd3884be18176",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-2.006003.tar.gz",
    )

    provides("perl-sub-defer")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal@0.3:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-name@0.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack

