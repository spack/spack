# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelCaller(PerlPackage):
    """Meatier versions of caller."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Devel-Caller-2.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.06", sha256="6a73ae6a292834255b90da9409205425305fcfe994b148dcb6d2d6ef628db7df")
    version("2.05", sha256="dcfb590044277e125e78f781a150198a94c89769af6faab8f544a916dfbb4388")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-padwalker@0.8:", type="run")  # AUTO-CPAN2Spack
