# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathComplex(PerlPackage):
    """Trigonometric functions."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Math-Complex-1.59.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.59", sha256="f35eb4987512c51d2c47294a008ede210d8dd759b90b887d04847c69b42dd6d1")
    version("1.58", sha256="304511599eb997fde7e21f7ea4105f0882f7cddb94537f56d2a46d618a8bb3d8")

    provides("perl-math-trig@1.23")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.11:", type="run")  # AUTO-CPAN2Spack
