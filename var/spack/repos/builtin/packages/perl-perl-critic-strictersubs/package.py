# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticStrictersubs(PerlPackage):
    """Perl::Critic plugin for stricter subroutine checking."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Perl-Critic-StricterSubs-0.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.06", sha256="bdf438b7b29c6699fbdea317400ae4b8d28a2078b21c51c9afe8e06c96c9ca77")

    depends_on("perl-module-build", type="build")

    provides("perl-perl-critic-policy-modules-requireexplicitinclusion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitcallstoundeclaredsubs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitcallstounexportedsubs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitexportingundeclaredsubs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitqualifiedsubdeclarations")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-strictersubs-utils")  # AUTO-CPAN2Spack
    depends_on("perl-file-pathlist", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.4:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils@1.82:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils", type="run")  # AUTO-CPAN2Spack

