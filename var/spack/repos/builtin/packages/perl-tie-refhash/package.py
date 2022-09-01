# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTieRefhash(PerlPackage):
    """Use references as hash keys."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/karenetheridge/Tie-RefHash"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Tie-RefHash-1.40.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.40", sha256="5acf1f518d2fb5f620caad7a1b2ff1f6f7516fef8f40ba6b743eec8b96927ed7")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="test")  # AUTO-CPAN2Spack
