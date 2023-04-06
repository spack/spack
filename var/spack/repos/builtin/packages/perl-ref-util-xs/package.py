# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRefUtilXs(PerlPackage):
    """XS implementation for Ref::Util."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/Ref-Util-XS-0.117.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.117", sha256="fb64c5a823787f6600257918febd9fbc6f0305936fc3287b81a30c099b65633c")
    version("0.116", sha256="cee4aa858f89a667f202c702d87c8c6e5d837341e64cd91cda94c570dafaad50")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
