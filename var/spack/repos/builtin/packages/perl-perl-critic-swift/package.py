# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticSwift(PerlPackage):
    """A set of additional policies for Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/E/EL/ELLIOTJS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/EL/ELLIOTJS/Perl-Critic-Swift-v1.0.3.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.0.3", sha256="eb8a36c11ef75df2ac4428f5311168e3e8425a25f593c271d09de20700f8d89d")
    version("1.0.2", sha256="14cf4b14a541c4f8a0746529c43a262b68ee5fa8a156c2b6aaa4ffc5c16616dc")

    depends_on("perl-module-build", type="build")

    provides("perl-perl-critic-policy-codelayout-requireuseutf8")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirepoduseencodingutf8")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.28.8:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-perl-critic@1.1:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils@0.21:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-testutils@1.82:", type="build")  # AUTO-CPAN2Spack

