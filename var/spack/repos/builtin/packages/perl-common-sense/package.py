# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCommonSense(PerlPackage):
    """Save a tree AND a kitten, use common::sense!."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/common-sense-3.75.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("3.75", sha256="a86a1c4ca4f3006d7479064425a09fa5b6689e57261fcb994fe67d061cba0e7e")
    version("3.74", sha256="771f7d02abd1ded94d9e37d3f66e795c8d2026d04defbeb5b679ca058116bbf3")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
