# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticTics(PerlPackage):
    """Policies for things that make me wince."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/rjbs/Perl-Critic-Tics"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Perl-Critic-Tics-0.009.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.009", sha256="7542662b56622f5d646b00068c8f9befbc16e462228a0cd47d54549d24eb7493")
    version("0.008", sha256="26bfa6dff571061c71e9914a71d90ae02e661bfac0943cf60ae5085c86766999")

    provides("perl-perl-critic-policy-tics-prohibitlonglines")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-tics-prohibitmanyarrows")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-tics-prohibitusebase")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.30:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-violation", type="run")  # AUTO-CPAN2Spack
