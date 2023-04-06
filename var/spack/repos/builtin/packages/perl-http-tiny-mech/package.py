# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpTinyMech(PerlPackage):
    """Wrap a WWW::Mechanize instance in an HTTP::Tiny compatible interface.."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/kentnl/HTTP-Tiny-Mech"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KE/KENTNL/HTTP-Tiny-Mech-1.001002.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "1.001.002",
        sha256="ed3b428307c678b9ddf27c180490c58d75da19b3d83c1269fd44a4054fed6c24",
        url="https://cpan.metacpan.org/authors/id/K/KE/KENTNL/HTTP-Tiny-Mech-1.001002.tar.gz",
    )
    version(
        "1.001.001",
        sha256="0bf8dd1850e0722f60ea56e5213d06f96326673300421f7cea5df735aab4590a",
        url="https://cpan.metacpan.org/authors/id/K/KE/KENTNL/HTTP-Tiny-Mech-1.001001.tar.gz",
    )

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-response", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-www-mechanize", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@7.0:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-request", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-tiny@0.22:", type=("run", "test"))  # AUTO-CPAN2Spack
