# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelStacktrace(PerlPackage):
    """An object representing a stack trace."""

    homepage = "https://metacpan.org/pod/Devel::StackTrace"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Devel-StackTrace-2.02.tar.gz"

    version("2.04", sha256="cd3c03ed547d3d42c61fa5814c98296139392e7971c092e09a431f2c9f5d6855")
    version("2.03", sha256="7618cd4ebe24e254c17085f4b418784ab503cb4cb3baf8f48a7be894e59ba848")
    version("2.02", sha256="cbbd96db0ecf194ed140198090eaea0e327d9a378a4aa15f9a34b3138a91931f")
    provides("perl-devel-stacktrace-frame")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
