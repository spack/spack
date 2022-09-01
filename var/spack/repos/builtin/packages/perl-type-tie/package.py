# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypeTie(PerlPackage):
    """Tie a variable to a type constraint."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Type-Tie"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tie-0.015.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.015", sha256="4e5a3f6737efd59b4e395af2f95d02e564fc57aa723e32a13eb2a1788d6d5434")
    version("0.014", sha256="b5359514b8ee82d3ee07f65eb22dfe27ad4b2296161294264d65b53c561f22e6")

    provides("perl-type-nano")  # AUTO-CPAN2Spack
    provides("perl-type-tie-array")  # AUTO-CPAN2Spack
    provides("perl-type-tie-base")  # AUTO-CPAN2Spack
    provides("perl-type-tie-hash")  # AUTO-CPAN2Spack
    provides("perl-type-tie-scalar")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-exporter-tiny@0.26:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-hash-fieldhash", type="run")  # AUTO-CPAN2Spack

