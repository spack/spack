# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlReadonlyXs(PerlPackage):
    """Companion module for Readonly.pm,
    to speed up read-only scalar variables."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RO/ROODE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RO/ROODE/Readonly-XS-1.05.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.05", sha256="8ae5c4e85299e5c8bddd1b196f2eea38f00709e0dc0cb60454dc9114ae3fff0d")
    version("1.04", sha256="3dce369ffcdaccd37e7ae65ce5a1dcda33dc99d91f8b8629265cf300898c41a4")

    depends_on("perl-readonly@1.2:", type="run")  # AUTO-CPAN2Spack
