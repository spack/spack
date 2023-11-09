# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSharedir(PerlPackage):
    """File::ShareDir - Locate per-dist and per-module shared files"""

    homepage = "https://metacpan.org/pod/File::ShareDir"
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-ShareDir-1.118.tar.gz"

    version("1.118", sha256="3bb2a20ba35df958dc0a4f2306fc05d903d8b8c4de3c8beefce17739d281c958")

    # depends_on("perl-module-build", type="build")
