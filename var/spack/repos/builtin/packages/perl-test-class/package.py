# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestClass(PerlPackage):
    """Easily create test classes in an xUnit/JUnit style."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SZ/SZABGAB"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SZ/SZABGAB/Test-Class-0.52.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.52", sha256="40c1b1d388f0a8674769c27529f0cc3634ca0fd9d8f72b196c0531611934bc82")

    provides("perl-test-class-load")  # AUTO-CPAN2Spack
    provides("perl-test-class-methodinfo")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-mro-compat@0.11:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-attribute-handlers@0.77:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-runtime", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-exception@0.25:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-try-tiny", type="run")  # AUTO-CPAN2Spack

