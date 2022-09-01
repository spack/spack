# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestSha1(PerlPackage):
    """Perl interface to the SHA-1 algorithm."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/G/GA/GAAS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/G/GA/GAAS/Digest-SHA1-2.13.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.13", sha256="68c1dac2187421f0eb7abf71452a06f190181b8fc4b28ededf5b90296fb943cc")
    version("2.12", sha256="aa13440259fd7e0a343b343b428f514791007f4a2e1b268007f9a6e5c75af5a5")

    depends_on("perl@5.4:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

