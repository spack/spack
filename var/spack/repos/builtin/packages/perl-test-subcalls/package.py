# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestSubcalls(PerlPackage):
    """Track the number of times subs are called."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/karenetheridge/Test-SubCalls"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-SubCalls-1.10.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.10", sha256="cbc1e9b35a05e71febc13e5ef547a31c8249899bb6011dbdc9d9ff366ddab6c2")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-hook-lexwrap@0.20:", type="run")  # AUTO-CPAN2Spack
