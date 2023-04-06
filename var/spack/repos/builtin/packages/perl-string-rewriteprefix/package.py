# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringRewriteprefix(PerlPackage):
    """Rewrite strings based on a set of known prefixes."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/rjbs/String-RewritePrefix"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/String-RewritePrefix-0.008.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.008", sha256="e45a31d6914e8f5fc722ef48d8819400dafc02105e0c61414aabbf01bce208eb")
    version("0.007", sha256="5cbbccd5636315a90ddec3610c718411b971ae4b74d5e9e2c9a0b3f976a0dda2")

    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-sub-exporter@0.972:", type="run")  # AUTO-CPAN2Spack
