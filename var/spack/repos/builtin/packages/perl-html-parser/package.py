# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlParser(PerlPackage):
    """HTML parser class"""

    homepage = "https://metacpan.org/pod/HTML::Parser"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTML-Parser-3.78.tar.gz"

    version("3.78", sha256="22564002f206af94c1dd8535f02b0d9735125d9ebe89dd0ff9cd6c000e29c29d")
    version("3.77", sha256="792a6e314f8eb0e87be7f5fdcf1b0c170a26a0e53da48d9a315db76f876949f3")
    version("3.76", sha256="64d9e2eb2b420f1492da01ec0e6976363245b4be9290f03f10b7d2cb63fa2f61")
    version("3.72", sha256="ec28c7e1d9e67c45eca197077f7cdc41ead1bb4c538c7f02a3296a4bb92f608b",
        url="https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTML-Parser-3.72.tar.gz")

    provides("perl-html-entities")  # AUTO-CPAN2Spack
    provides("perl-html-filter")  # AUTO-CPAN2Spack
    provides("perl-html-headparser")  # AUTO-CPAN2Spack
    provides("perl-html-linkextor")  # AUTO-CPAN2Spack
    provides("perl-html-pullparser")  # AUTO-CPAN2Spack
    provides("perl-html-tokeparser")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-uri", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-uri-url", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.52:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-html-tagset", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-headers", type="run")  # AUTO-CPAN2Spack
