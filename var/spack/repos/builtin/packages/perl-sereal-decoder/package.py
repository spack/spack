# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSerealDecoder(PerlPackage):
    """Fast, compact, powerful binary deserialization."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/Y/YV/YVES"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Decoder-4.025.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("5.001", sha256="b27c33ec910de57d72817cc2baa0bf039d5e647a7359edfcf1cf7d5efeeed9b2")
    version("5.000_002", sha256="abe866ec8480a364745d00b8980d8f866dd0edd1420102e9e5ed82e932269507")
    version("4.025", sha256="8e0e3b9a9af1a778b7de21506fa30797fb1b520dcd002f3f29e6dcb52446dea5")

    provides("perl-sereal-decoder-constants")  # AUTO-CPAN2Spack
    provides("perl-sereal-performance")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-parsexs@2.21:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@7.0:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-longstring", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-differences", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-warn", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack
