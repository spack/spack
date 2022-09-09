# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringFormat(PerlPackage):
    """Sprintf-like string formatting capabilities with
    arbitrary format definitions."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SR/SREZIC"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SR/SREZIC/String-Format-1.18.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.18", sha256="9e417a8f8d9ea623beea2d13a47c0d5a696fc8602c0509b826cd45f97b76e778")
    version("1.17_50", sha256="2dcd0ec5f0c7f67c6dd9d6de2c8c887ada3437f240ac4840d4d2196e01d47ac0")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
