# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleMask(PerlPackage):
    """Pretend certain modules are not installed."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/MA/MATTLAW"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/MA/MATTLAW/Module-Mask-0.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.06", sha256="2d73f81ff21c9fa28102791e546ff257164b3025f7832544c8223fb87c1e7e77")
    version("0.05", sha256="c7bfbd35d144412e5a213a2f4b6e2ad2885d93e71fdfb1f9bff467d75fb47eb7")

    depends_on("perl-module-build", type="build")

    depends_on("perl@5.8.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.40:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-pod-coverage@1.4:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-pod@1.14:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-util@1.0:", type="run")  # AUTO-CPAN2Spack
