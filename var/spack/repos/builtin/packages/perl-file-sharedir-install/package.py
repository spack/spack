# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSharedirInstall(PerlPackage):
    """Install shared files"""

    homepage = "https://metacpan.org/pod/File::ShareDir::Install"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-ShareDir-Install-0.11.tar.gz"

    version("0.14", sha256="8f9533b198f2d4a9a5288cbc7d224f7679ad05a7a8573745599789428bc5aea0")
    version("0.13", sha256="45befdf0d95cbefe7c25a1daf293d85f780d6d2576146546e6828aad26e580f9")
    version("0.12", sha256="9176dcf4aaeec3c64f259c671df8f7fda5040b38d9910858ae0353c19269e88d")
    version("0.11", sha256="32bf8772e9fea60866074b27ff31ab5bc3f88972d61915e84cbbb98455e00cc8")

    depends_on("perl-module-build", type="build")
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
