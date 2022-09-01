# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParDist(PerlPackage):
    """Create and manipulate PAR distributions."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/PAR-Dist-0.51.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.51", sha256="d242062df9b689f39040e4c4e09131a6c464d0eefadbd1c9ac947173af33dff8")
    version("0.50_001", sha256="cfacd0dc0816bae4bea5bd3c312a172928a9840bec5d16b7149600f93a29f3d0")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
