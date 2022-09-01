# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStatisticsDescriptive(PerlPackage):
    """Module of basic descriptive statistical functions."""

    homepage = "https://metacpan.org/pod/Statistics::Descriptive"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0612.tar.gz"

    version(
        "3.08.00",
        sha256="b04edeea26bfed435aa6029956798c281f7f52d4545f3f45b2ad44954e96f939",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0800.tar.gz",
    )
    version(
        "3.07.02",
        sha256="f98a10c625640170cdda408cccc72bdd7f66f8ebe5f59dec1b96185171ef11d0",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0702.tar.gz",
    )
    version(
        "3.07.01",
        sha256="35b09ed91b8660a6095c272a36ed2c61b3c660aa535fc23a20beadf7769e1919",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0701.tar.gz",
    )
    version(
        "3.07.00",
        sha256="2cddd1d0f764d0d8105806b12ca344961fecf26f97da6769b59fc086d684fd67",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0700.tar.gz",
    )
