# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSafeIsa(PerlPackage):
    """Call isa, can, does and DOES safely on things that may not be objects."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/E/ET/ETHER"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Safe-Isa-1.000010.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "1.000.010",
        sha256="87f4148aa0ff1d5e652723322eab7dafa3801c967d6f91ac9147a3c467b8a66a",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Safe-Isa-1.000010.tar.gz",
    )
    version(
        "1.000.009",
        sha256="510770f2e32c22532b8c162641fb989c7d2b143a4b316e69a34ad5415135a65f",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Safe-Isa-1.000009.tar.gz",
    )

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack

