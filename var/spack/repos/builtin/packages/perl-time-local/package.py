# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeLocal(PerlPackage):
    """Efficiently compute time from local and GMT time."""  # AUTO-CPAN2Spack

    homepage = "http://metacpan.org/release/Time-Local"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Time-Local-1.30.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "1.31-TRIAL",
        sha256="c5acfe5de04af6ebb69dd8dec17788594e32053c8b8f7e4c43f823019cd72f83",
    )  # Pre-release.
    version(
        "1.30",
        sha256="c7744f6b2986b946d3e2cf034df371bee16cdbafe53e945abb1a542c4f8920cb",
        preferred=True,
    )
    version(
        "1.29-TRIAL", sha256="a942586c702730addccea62e2721c3b13df672c08c92101d5743d7529ccb8ae8"
    )
    version("1.28", sha256="9278b9e5cc99dcbb0fd27a43e914828b59685601edae082889b5ee7266afe10e")
    version("1.27", sha256="926b6b270209d508226b4f0e24d0e13c12cb94b81479e100d796beb45f9bcc1e")

    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
