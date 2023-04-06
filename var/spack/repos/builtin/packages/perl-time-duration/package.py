# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeDuration(PerlPackage):
    """Rounded or exact English expression of durations."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/neilbowers/Time-Duration"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Time-Duration-1.21.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.21", sha256="fe340eba8765f9263694674e5dff14833443e19865e5ff427bbd79b7b5f8a9b8")
    version("1.20", sha256="458205b528818e741757b2854afac5f9af257f983000aae0c0b1d04b5a9cbbb8")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
