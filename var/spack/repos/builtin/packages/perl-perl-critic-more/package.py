# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticMore(PerlPackage):
    """Supplemental policies for Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TH/THALJEF/Perl-Critic-More-1.003.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.003", sha256="69e2acff61b7bead745721991e2b83c88624ae8239d4371a785a3ce2d967187b")
    version("1.002", sha256="71cd154f311cb59df47df413efde460fa93b543eb6e7293080adfd3cc3050f8c")

    depends_on("perl-module-build", type="build")

    provides("perl-perl-critic-policy-codelayout-requireascii")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-editor-requireemacsfilevariables")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-errorhandling-requireuseofexceptions")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-perlminimumversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requireperlversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-requireconstantonleftsideofequality")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-restrictlongstrings")  # AUTO-CPAN2Spack
    depends_on("perl-readonly@1.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.4:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-minimumversion@0.14:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.98:", type="run")  # AUTO-CPAN2Spack

