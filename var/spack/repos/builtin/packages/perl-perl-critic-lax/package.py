# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticLax(PerlPackage):
    """Policies that let you slide on common exceptions."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/rjbs/Perl-Critic-Lax"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Perl-Critic-Lax-0.013.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.013", sha256="3f5619c209f93676e2fcdcd2990a27a5d77d2b0e60dcbdcd2680617355fd4620")
    version("0.012", sha256="47772ddbdd3c6ab00571c0ed8e95aeace705f725c650a572f060c30f7a96227a")

    provides(
        "perl-perl-critic-policy-lax-prohibitcomplexmappings-linesnotstatements"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-lax-prohibitemptyquotes-exceptasfallback")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-lax-prohibitleadingzeros-exceptchmod")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-lax-prohibitstringyeval-exceptforrequire")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-lax-requireconstantonleftsideofequality-excepteq"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-lax-requireendwithtrueconst")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-lax-requireexplicitpackage-exceptforpragmata"
    )  # AUTO-CPAN2Spack
    depends_on("perl-readonly", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on(
        "perl-perl-critic-policy-valuesandexpressions-prohibitleadingzeros", type="run"
    )  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.88:", type="run")  # AUTO-CPAN2Spack
