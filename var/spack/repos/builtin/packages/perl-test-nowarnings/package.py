# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestNowarnings(PerlPackage):
    """Make sure you didn't emit any warnings while testing."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/H/HA/HAARG"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-NoWarnings-1.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.06", sha256="c2dc51143b7eb63231210e27df20d2c8393772e0a333547ec8b7a205ed62f737")
    version("1.05_01", sha256="f8d4d7525f2dedee1cf15cda520382500c992bbcbfbc8e5fac1820ca13de8783")

    provides("perl-test-nowarnings-warning")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
