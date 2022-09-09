# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTieFile(PerlPackage):
    """Access the lines of a disk file via a Perl array."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/T/TO/TODDR"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/Tie-File-1.05.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.05", sha256="8a980b577ff4b10fe11062ed8c774857fa8c9833c5305f2e8bfb3347af63f139")
    version("1.04", sha256="a3ead2905587e532b9b40094d1dcfcfcc895b01c57b551d9a91bdce450cc4361")

    provides("perl-tie-file-cache")  # AUTO-CPAN2Spack
    provides("perl-tie-file-heap")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
