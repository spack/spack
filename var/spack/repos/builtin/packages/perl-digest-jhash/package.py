# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestJhash(PerlPackage):
    """Perl extension for 32 bit Jenkins Hashing Algorithm."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Digest-JHash-0.10.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.10", sha256="c746cf0a861a004090263cd54d7728d0c7595a0cf90cbbfd8409b396ee3b0063")
    version("0.09", sha256="ba77919b7b7a1b6f222f1bb5a7a34d88b1a92093e40a2aec37352cb38926ada3")

    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-dynaloader", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
