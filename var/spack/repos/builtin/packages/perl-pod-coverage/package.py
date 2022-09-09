# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodCoverage(PerlPackage):
    """Checks if the documentation of a module is comprehensive."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-0.23.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.23", sha256="30b7a0b0c942f44a7552c0d34e9b1f2e0ba0b67955c61e3b1589ec369074b107")
    version("0.22", sha256="20adf0049c07c30046b0f881ab48f0d7efcd466732b86dad6c468ef4ed27b9f2")

    provides("perl-pod-coverage-countparents")  # AUTO-CPAN2Spack
    provides("perl-pod-coverage-exportonly")  # AUTO-CPAN2Spack
    provides("perl-pod-coverage-extractor")  # AUTO-CPAN2Spack
    provides("perl-pod-coverage-overloader")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-pod-find@0.21:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-devel-symdump@2.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-parser@1.13:", type="run")  # AUTO-CPAN2Spack
