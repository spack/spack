# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticDynamic(PerlPackage):
    """Dynamic policies for Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TH/THALJEF/Perl-Critic-Dynamic-0.05.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.05", sha256="4a4f05706abc46ae9c2f037f5d3fe01d987283214929bd01489f8ef9ed0f3df4")

    depends_on("perl-module-build", type="build")

    provides("perl-perl-critic-dynamicpolicy")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-dynamic-validateagainstsymboltable")  # AUTO-CPAN2Spack
    depends_on("perl-cgi", when="^perl@5.21:", type=("build", "test"))
    depends_on("perl-readonly", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy@1.108:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.36:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.108:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-devel-symdump@2.7:", type="run")  # AUTO-CPAN2Spack
