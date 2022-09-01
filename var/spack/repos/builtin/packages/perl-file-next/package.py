# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileNext(PerlPackage):
    """File-finding iterator."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/File-Next-1.18.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.18", sha256="f900cb39505eb6e168a9ca51a10b73f1bbde1914b923a09ecd72d9c02e6ec2ef")
    version("1.17_01", sha256="8b4b31369f3cc38ceceb87eb91e82c2d5b7923163a9f2bd005e621940a444a11")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

