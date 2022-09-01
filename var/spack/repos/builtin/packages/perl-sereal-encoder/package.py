# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSerealEncoder(PerlPackage):
    """Fast, compact, powerful binary serialization."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/Y/YV/YVES"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Encoder-4.025.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("5.001", sha256="2367f2f5f1486f32f65c3905048918de55639c79d1835ab56789f70cedfbbac3")
    version("4.025", sha256="0fd51ba6083026650d08526758261173c18ab8234c5526fac7edb91ad9c6026e")

    provides("perl-sereal-encoder-constants")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-parsexs@2.21:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-sereal-decoder@5.0:", type=("build", "test"), when="@5.0:")
    depends_on("perl-sereal-decoder@:4.999999", type=("build", "test"), when="@:4.999999")
    depends_on("perl-test-longstring", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@7.0:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-differences", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-warn", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack
