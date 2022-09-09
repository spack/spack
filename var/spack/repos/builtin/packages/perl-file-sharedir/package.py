# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSharedir(PerlPackage):
    """Locate per-dist and per-module shared files."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/File-ShareDir"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-ShareDir-1.118.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.118", sha256="3bb2a20ba35df958dc0a4f2306fc05d903d8b8c4de3c8beefce17739d281c958")
    version("1.117_001", sha256="15bef8c556a7b426760586f8ec13e1cca775b8f76f4db54acd99250e0b56a990")

    depends_on("perl-params-util@1.7:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-inspector@1.12:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils@0.428:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-sharedir-install@0.13:", type="build")  # AUTO-CPAN2Spack
