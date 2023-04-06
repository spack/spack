# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PerlPerlCriticPetpeevesJtrammell(PerlPackage):
    """Policies to prohibit/require my pet peeves."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/J/JT/JTRAMMELL"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/J/JT/JTRAMMELL/Perl-Critic-PetPeeves-JTRAMMELL-0.04.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.04", sha256="fb931eb3434b6b75339d079a469f7a389269df155f46ee5e7cc60c2ebbae4a04")
    version("0.03", sha256="756671be54d026aa018527285d32205c83080fe32d0d60bb947c254455a46e18")

    provides(
        "perl-perl-critic-policy-variables-prohibituselessinitialization@0.02"
    )  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.35:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-config", type="build")  # AUTO-CPAN2Spack

    @run_before("configure")
    def remove_bad_Makefile_PL(self):
        os.remove("Makefile.PL")
