# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathBigint(PerlPackage):
    """Math::BigInt - arbitrary size integer math package"""

    homepage = "https://metacpan.org/pod/Math::BigInt"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999837.tar.gz"

    version(
        "1.999.838",
        sha256="d3c2fb37d412ac8d126452caad5764f02193147261b59c56e652167c41d1e9d5",
        url="https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999838.tar.gz",
    )
    version(
        "1.999.837",
        sha256="038f9aad6318f20a84a7b1afe3087a1b02406c9988ce5919311a797f85a32962",
        url="https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999837.tar.gz",
    )
    version(
        "1.999.836",
        sha256="9f0ffeed664d5576e2b5df6d2e2255643e9c4b5108f9be053c9ea137c020bbfe",
        url="https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999836.tar.gz",
    )

    provides("perl-math-bigfloat")
    provides("perl-math-bigint-calc")
    provides("perl-math-bigint-lib")
    depends_on("perl@5.6.1:", type="run")
    depends_on("perl-extutils-makemaker@6.58:", type="build")
    depends_on("perl-scalar-util", type="run")
    depends_on("perl-math-complex@1.36:", type="run")
