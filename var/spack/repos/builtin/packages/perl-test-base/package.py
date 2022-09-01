# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestBase(PerlPackage):
    """A Data Driven Testing Framework."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/ingydotnet/test-base-pm"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/I/IN/INGY/Test-Base-0.89.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.89", sha256="2794a1aaaeb1d3a287dd2c7286258663796562f7db9ccc6b424bc4f1de8ad014")
    version("0.88", sha256="52368cc5a9cbbc4eaba33ed820672f92001b73d8bcba0bb95d5fdb1d370b9039")

    provides("perl-test-base-block")  # AUTO-CPAN2Spack
    provides("perl-test-base-filter")  # AUTO-CPAN2Spack
    provides("perl-test-base-handle")  # AUTO-CPAN2Spack
    depends_on("perl-text-diff@0.35:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.52:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-algorithm-diff@1.15:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.7:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-filter-util-call", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-spiffy@0.40:", type="run")  # AUTO-CPAN2Spack

