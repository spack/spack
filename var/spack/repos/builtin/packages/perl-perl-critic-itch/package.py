# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticItch(PerlPackage):
    """Perl::Critic::Itch - A collection of Policies to solve some Itches."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/MA/MARCELO"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/MA/MARCELO/Perl-Critic-Itch-0.07.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.0", sha256="e95dda38dc5120656f01a49b0df34346c9a2d9b03b021f3aeb7dfe5167c2d0c4")
    version("0.07", sha256="f3151b35fbe664bfbae6b2996f22666f6908988c2c2cd813a212b5321e571061")

    provides("perl-perl-critic-policy-codelayout-prohibithashbarewords")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.52:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils@1.52:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-violation@1.52:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.52:", type="run")  # AUTO-CPAN2Spack

