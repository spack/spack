# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlOstype(PerlPackage):
    """Map Perl operating system names to generic types."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Perl-Toolchain-Gang/Perl-OSType"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Perl-OSType-1.010.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.010", sha256="e7ed4994b5d547cb23aadb84dc6044c5eb085d5a67a6c5624f42542edd3403b2")
    version("1.009", sha256="245cf4c9f7614ac5e5c3bc82621fa2ab4f3c25e0aaae3016b7eed5d40ddcae06")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
