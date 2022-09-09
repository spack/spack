# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticNits(PerlPackage):
    """Policies of nits I like to pick."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/K/KC/KCOWGILL"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KC/KCOWGILL/Perl-Critic-Nits-v1.0.0.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.0.0", sha256="92fc3635711e48981240d5c5c4205377f89a46bbbe86eb8d79a26f2744d7450f")

    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitaccessofprivatedata"
    )  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.7:", type="run")  # AUTO-CPAN2Spack
