# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpCookies(PerlPackage):
    """HTTP cookie jars"""

    homepage = "https://metacpan.org/pod/HTTP::Cookies"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Cookies-6.04.tar.gz"

    version("6.10", sha256="e36f36633c5ce6b5e4b876ffcf74787cc5efe0736dd7f487bdd73c14f0bd7007")
    version("6.09", sha256="903f017afaa5b78599cc90efc14ecccc8cc2ebfb636eb8c02f8f16ba861d1fe0")
    version("6.08", sha256="49ebb73576eb41063c04bc079477df094496deec805ae033f3be338c23c3af59")
    version("6.07", sha256="6a2f8cde56074c9dc5b46a143975f19b981d0569f1d4dc5e80567d6aab3eea2a")
    version("6.06", sha256="e7f4872f24025657db809eee652449d348e57c9496281fb3727aed31c4f8368f")
    version("6.05", sha256="58e1cd041bfcf33c2ab4140de7a757234809b8cf072afa727a6f3ffe84b66f5d")
    version("6.04", sha256="0cc7f079079dcad8293fea36875ef58dd1bfd75ce1a6c244cd73ed9523eb13d4")

    provides("perl-http-cookies-microsoft")  # AUTO-CPAN2Spack
    provides("perl-http-cookies-netscape")  # AUTO-CPAN2Spack
    depends_on("perl-uri", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-response", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-headers-util@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-date@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-request", type="run")  # AUTO-CPAN2Spack
