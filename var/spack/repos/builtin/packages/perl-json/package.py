# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJson(PerlPackage):
    """JSON (JavaScript Object Notation) encoder/decoder"""

    homepage = "https://metacpan.org/pod/JSON"
    url = "https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-4.09.tar.gz"

    version("4.09", sha256="6780a51f438c0932eec0534fc9cd2b1ad0d64817eda4add8ede5ec77d6d2c991")
    version("4.08", sha256="6b2a38eb6f92934840d142e31ce6683610b66477fad3ffab1111978ef26ca53f")

    provides("perl-json-backend-pp")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-json-xs@2.34:", type="run")  # AUTO-CPAN2Spack
