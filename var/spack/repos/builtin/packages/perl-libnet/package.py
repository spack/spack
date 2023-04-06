# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLibnet(PerlPackage):
    """Collection of network protocol modules."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SH/SHAY"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHAY/libnet-3.14.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("3.14", sha256="153c8eb8ef0f19cf2c631d5b45d05de98516937f34e261125ef242fba1fe2ea4")
    version("3.13", sha256="5a35fb1f2d4aa291680eb1af38899fab453c22c28e71f7c7bd3747b5a3db348c")

    depends_on("perl@5.8.1:", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.64:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-time-local", type="run")  # AUTO-CPAN2Spack
