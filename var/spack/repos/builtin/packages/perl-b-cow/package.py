# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBCow(PerlPackage):
    """B::COW additional B helpers to check COW status."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/B-COW-0.004.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.004", sha256="fcafb775ed84a45bc2c06c5ffd71342cb3c06fb0bdcd5c1b51b0c12f8b585f51")
    version("0.003", sha256="9c7de86542871bc0ac8e6b4f7363bba4f6c5cc07e06fadc51d3a78832fcfca89")

    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack

