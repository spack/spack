# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticBangs(PerlPackage):
    """Perl::Critic::Bangs - A collection of policies for Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Perl-Critic-Bangs-1.12.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.12", sha256="73242b27da2feb601e4a47e7975d864df7279317f1b0565474be3cfc31bfa119")
    version("1.11_03", sha256="420b5cd5faf96405d1040f3e896e8811a691ba73ba3b75058b6ac4efc6e1f27a")

    provides("perl-perl-critic-policy-bangs-prohibitbitwiseoperators")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitcommentedoutcode")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitdebuggingmodules")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitflagcomments")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitnoplan")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitnumberednames")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitrefprotoorproto")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibituselessregexmodifiers")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-bangs-prohibitvaguenames")  # AUTO-CPAN2Spack
    depends_on("perl-readonly", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policyfactory", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-perl-critic@1.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policyparameter", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-cache", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-violation", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.122:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-userprofile", type="run")  # AUTO-CPAN2Spack

