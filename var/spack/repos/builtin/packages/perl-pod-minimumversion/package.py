# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodMinimumversion(PerlPackage):
    """Determine minimum Perl version of POD directives."""  # AUTO-CPAN2Spack

    homepage = "http://user42.tuxfamily.org/pod-minimumversion/index.html"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KR/KRYDE/Pod-MinimumVersion-50.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("50", sha256="0bd2812d9aacbd99bb71fa103a4bb129e955c138ba7598734207dc9fb67b5a6f")
    version("49", sha256="6226fc64d8c776c1025e6d074d811732b64ae6dba22c00bf1f4eaac05b23c8d7")

    provides("perl-pod-minimumversion-parser")  # AUTO-CPAN2Spack
    provides("perl-pod-minimumversion-report")  # AUTO-CPAN2Spack
    depends_on("perl@5.4:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-string@1.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-parser", type="run")  # AUTO-CPAN2Spack
