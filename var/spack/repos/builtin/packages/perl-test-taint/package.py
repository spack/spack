# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestTaint(PerlPackage):
    """Checks for taintedness of variables."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Test-Taint-1.08.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.08", sha256="5d594d4257352c93785024c63aa0a7b73d912ceca9611cd975ce83aab021a97d")
    version("1.06", sha256="721b51ca91d248ea5ff4f99ca49c05a080e6f0fc9f7983e96121b7775ab93107")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack

