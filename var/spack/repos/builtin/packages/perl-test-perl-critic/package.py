# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestPerlCritic(PerlPackage):
    """Use Perl::Critic in test programs."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Test-Perl-Critic-1.04.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.04", sha256="28f806b5412c7908b56cf1673084b8b44ce1cb54c9417d784d91428e1a04096e")

    depends_on("perl-module-build", type="build")

    depends_on("perl-module-build@0.4:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.105:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-mce@1.827:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-violation@1.105:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.105:", type="run")  # AUTO-CPAN2Spack
