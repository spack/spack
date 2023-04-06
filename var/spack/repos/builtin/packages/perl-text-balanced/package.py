# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextBalanced(PerlPackage):
    """Extract delimited text sequences from strings.."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SH/SHAY"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHAY/Text-Balanced-2.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.06", sha256="773e0f0f21c0cb2cf664cee6ba28ff70259babcc892f9b650f9cbda00be092ad")
    version("2.05", sha256="3a6f3fbcc6cb5406964b2e332688bae3c2595436d03ddb25ee6703a47a98977d")

    provides("perl-text-balanced-errormsg")  # AUTO-CPAN2Spack
    provides("perl-text-balanced-extractor")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.64:", type="build")  # AUTO-CPAN2Spack
