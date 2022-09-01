# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStrictures(PerlPackage):
    """Turn on strict and make most warnings fatal."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/H/HA/HAARG"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/strictures-2.000006.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "2.000.006",
        sha256="09d57974a6d1b2380c802870fed471108f51170da81458e2751859f2714f8d57",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/strictures-2.000006.tar.gz",
    )
    version(
        "2.000.004",
        sha256="23842430a3fe1d664aa9399a7356b0463a24fe4f7ed3f68f7bdb4c3e0d06f753",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/strictures-2.000004.tar.gz",
    )

    provides("perl-strictures-extra")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
