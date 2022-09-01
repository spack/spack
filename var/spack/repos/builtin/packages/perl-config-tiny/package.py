# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigTiny(PerlPackage):
    """Read/Write .ini style files with as little code as possible."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Config-Tiny-2.28.tgz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.28", sha256="12df843a0d29d48f61bcc14c4f18f0858fd27a8dd829a00319529d654fe01500")
    version("2.27", sha256="38b01b7014223a2890acdb84d67b08bfd6ddbd91b34e0de613b87cd961e0629d")

    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-pod@1.51:", type=("build", "test"))  # AUTO-CPAN2Spack

