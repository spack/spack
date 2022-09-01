# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileListing(PerlPackage):
    """Parse directory listing"""

    homepage = "https://metacpan.org/pod/File::Listing"
    url = "https://cpan.metacpan.org/authors/id/G/GA/GAAS/File-Listing-6.04.tar.gz"

    version("6.04", sha256="1e0050fcd6789a2179ec0db282bf1e90fb92be35d1171588bd9c47d52d959cf5")

    provides("perl-file-listing-apache")  # AUTO-CPAN2Spack
    provides("perl-file-listing-dosftp")  # AUTO-CPAN2Spack
    provides("perl-file-listing-netware")  # AUTO-CPAN2Spack
    provides("perl-file-listing-unix")  # AUTO-CPAN2Spack
    provides("perl-file-listing-vms")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-http-date", type="run")  # AUTO-CPAN2Spack
