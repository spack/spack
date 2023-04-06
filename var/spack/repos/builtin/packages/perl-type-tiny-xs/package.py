# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypeTinyXs(PerlPackage):
    """Provides an XS boost for some of Type::Tiny's built-in type
    constraints."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Type-Tiny-XS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-XS-0.022.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.022", sha256="bcc34a31f7dc1d30cc803889b5c8f90e4773b73b5becbdb3860f5abe7e22ff00")
    version("0.021", sha256="f7a9e216d1496744def402aa326620e13e73ad1ee7109cfbaeaac363d8eaf5df")

    provides("perl-type-tiny-xs-util")  # AUTO-CPAN2Spack
    depends_on("perl@5.10.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
