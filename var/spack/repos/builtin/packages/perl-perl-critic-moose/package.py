# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticMoose(PerlPackage):
    """Policies for Perl::Critic concerned with using Moose."""  # AUTO-CPAN2Spack

    homepage = "http://metacpan.org/release/Perl-Critic-Moose"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Perl-Critic-Moose-1.05.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.05", sha256="52eb8e22c42643f17fe297a21714017efdb9e2986c24e3337e030f3650f92201")
    version("1.04", sha256="7a441cd9e08090c3e676c904e452efeff6f42f171cd38c5e2e609f8c45692a3d")

    provides("perl-perl-critic-policy-moose-prohibitdestroymethod")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-moose-prohibitlazybuild")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-moose-prohibitmultiplewiths")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-moose-prohibitnewmethod")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-moose-requirecleannamespace")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-moose-requiremakeimmutable")  # AUTO-CPAN2Spack
    depends_on("perl-readonly", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-namespace-autoclean", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-perl-critic-policy", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils-ppi", type="run")  # AUTO-CPAN2Spack
