# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFilter(PerlPackage):
    """Source Filters."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Filter-1.64.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.64", sha256="13e7fb7e1d326598e3660103cf1974bee9f690ac5b43b339f2c022f2b5fcef2c")
    version("1.63", sha256="b667f5693e4608d908e2cf4527fa84f2a858f015b16c344b6961b0090f63670c")

    provides("perl-filter-util-call")  # AUTO-CPAN2Spack
    provides("perl-filter-util-exec")  # AUTO-CPAN2Spack
    provides("perl-filter-cpp")  # AUTO-CPAN2Spack
    provides("perl-filter-decrypt")  # AUTO-CPAN2Spack
    provides("perl-filter-exec")  # AUTO-CPAN2Spack
    provides("perl-filter-m4")  # AUTO-CPAN2Spack
    provides("perl-filter-sh")  # AUTO-CPAN2Spack
    provides("perl-filter-tee")  # AUTO-CPAN2Spack
    depends_on("perl-filter-simple@0.88:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
