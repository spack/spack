# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextAbbrev(PerlPackage):
    """Abbrev - create an abbreviation table from a list."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/dist/Text-Abbrev"
    url = "https://cpan.metacpan.org/authors/id/F/FL/FLORA/Text-Abbrev-1.02.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.02", sha256="9cfb8bea2d5806b72fa1a0e1a3367ce662262eaa2701c6a3143a2a8076917433")
    version("1.01", sha256="7017c72e8edb69842a623226ac1153c9e0f172ac1a7c2fc4c65631f4dd8fa748")

    depends_on("perl@5.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.30:", type="build")  # AUTO-CPAN2Spack
