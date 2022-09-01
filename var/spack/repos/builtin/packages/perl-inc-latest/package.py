# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIncLatest(PerlPackage):
    """Use modules bundled in inc/ if they are newer than installed ones."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/dagolden/inc-latest"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/inc-latest-0.500.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.500", sha256="daa905f363c6a748deb7c408473870563fcac79b9e3e95b26e130a4a8dc3c611")

    provides("perl-inc-latest-private")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("run", "test"))  # AUTO-CPAN2Spack

