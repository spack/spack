# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixQuotelike(PerlPackage):
    """Parse Perl string literals and string-literal-like things."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/W/WY/WYANT"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-QuoteLike-0.022.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.022", sha256="e043488d3b561b65188ab8e7b778f682490bf710a7bddced521e77bd111d378a")
    version("0.021_01", sha256="72df53114cb6fb0bf847c0073b35bc8a3097fcdf4cbadd451174fb960787b9af")

    depends_on("perl-module-build", type="build")

    provides("perl-ppix-quotelike-constant")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-dumper")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-control")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-delimiter")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-interpolation")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-string")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-structure")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-token-whitespace")  # AUTO-CPAN2Spack
    provides("perl-ppix-quotelike-utils")  # AUTO-CPAN2Spack
    depends_on("perl-readonly", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-dumper@1.238:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document@1.238:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
