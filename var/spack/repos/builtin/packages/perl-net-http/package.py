# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetHttp(PerlPackage):
    """Low-level HTTP connection (client)"""

    homepage = "https://metacpan.org/pod/Net::HTTP"
    url = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/Net-HTTP-6.17.tar.gz"

    version("6.22", sha256="62faf9a5b84235443fe18f780e69cecf057dea3de271d7d8a0ba72724458a1a2")
    version("6.17", sha256="1e8624b1618dc6f7f605f5545643ebb9b833930f4d7485d4124aa2f2f26d1611")

    depends_on("perl-uri", type=("build", "run"))
