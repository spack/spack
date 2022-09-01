# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestYaml(PerlPackage):
    """Testing Module for YAML Implementations."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/ingydotnet/test-yaml-pm"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TI/TINITA/Test-YAML-1.07.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.07", sha256="1f300d034f46298cb92960912cc04bac33fb27f05b8852d8f051e110b9cd995f")

    provides("perl-test-yaml-filter")  # AUTO-CPAN2Spack
    depends_on("perl-test-base@0.89:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

