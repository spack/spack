# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLwpMediatypes(PerlPackage):
    """Guess media type for a file or a URL"""

    homepage = "https://metacpan.org/pod/LWP::MediaTypes"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-6.04.tar.gz"

    version("6.04", sha256="8f1bca12dab16a1c2a7c03a49c5e58cce41a6fec9519f0aadfba8dad997919d9")
    version(
        "6.02",
        sha256="18790b0cc5f0a51468495c3847b16738f785a2d460403595001e0b932e5db676",
        url="https://cpan.metacpan.org/authors/id/G/GA/GAAS/LWP-MediaTypes-6.02.tar.gz",
    )

    depends_on("perl-test-fatal", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.6.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
