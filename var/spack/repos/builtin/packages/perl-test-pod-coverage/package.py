# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestPodCoverage(PerlPackage):
    """Check for pod coverage in your distribution."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/N/NE/NEILB"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Test-Pod-Coverage-1.10.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.10", sha256="48c9cca9f7d99eee741176445b431adf09c029e1aa57c4703c9f46f7601d40d4")
    version("1.09_01", sha256="d0d5df9063bec4d652b780a4c39ddf48530f52c5f419146089b693b3ea265000")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-pod-coverage", type="run")  # AUTO-CPAN2Spack

