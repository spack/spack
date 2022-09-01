# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListMoreutilsXs(PerlPackage):
    """List::MoreUtils::XS is a backend for List::MoreUtils. Even if it's
    possible (because of user wishes) to have it practically independent from
    List::MoreUtils, it technically depend on List::MoreUtils. Since it's only
    a backend, the API is not public and can change without any warning."""

    homepage = "https://metacpan.org/pod/List::MoreUtils::XS"
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-XS-0.429_002.tar.gz"

    version("0.430", sha256="e8ce46d57c179eecd8758293e9400ff300aaf20fefe0a9d15b9fe2302b9cb242")
    version("0.429_002", sha256="022c9663252c274384c61414dcf45e2c9c8292d15010825818b4305751fa1e39")
    version("0.429_001", sha256="1bb1e9673711f0ceaa1869430c5333fa43d2f72dd958c20f37677aa37d933aac")
    version("0.428", sha256="9d9fe621429dfe7cf2eb1299c192699ddebf060953e5ebdc1b4e293c6d6dd62d")
    depends_on("perl-test-leaktrace", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
