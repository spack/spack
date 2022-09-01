# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestMockrandom(PerlPackage):
    """Replaces random number generation with non-random number generation."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/dagolden/Test-MockRandom"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Test-MockRandom-1.01.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.01", sha256="2614930d84fc5deac39afbc1ee86ccd39b221507f27d4ee493ca26e5c921cce0")
    version("1.00", sha256="630bca40269d04520e39bb6579eb0399684cb17728702336ed1eb1542b7c2f97")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type=("build", "test"))  # AUTO-CPAN2Spack

