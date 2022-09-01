# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeDurationParse(PerlPackage):
    """Parse string that represents time duration."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/neilb/Time-Duration-Parse"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Time-Duration-Parse-0.16.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.16", sha256="1084a6463ee2790f99215bd76b135ca45afe2bfa6998fa6fd5470b69e1babc12")
    version("0.15", sha256="61d8143a8e6981cc1f7a974804d492039e5e56716767829d5e4bcd9ed74ae381")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-time-duration", type=("build", "test"))  # AUTO-CPAN2Spack

