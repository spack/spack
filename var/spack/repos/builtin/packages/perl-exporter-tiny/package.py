# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporterTiny(PerlPackage):
    """An exporter with the features of Sub::Exporter but only core
    dependencies"""

    homepage = "https://metacpan.org/pod/Exporter::Tiny"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.000000.tar.gz"

    version(
        "1.004.000",
        sha256="7f7b3b4fbe923355317243cd434d2319ffbad81c98cf8c8e189a6943b42bfeca",
        url="https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.004000.tar.gz",
    )
    version("1.003_002", sha256="d514973c97186a8d5e6d8e504ab4ed5154a915e28ab0b889f8fd38aa03869d43")
    version(
        "1.002.002",
        sha256="00f0b95716b18157132c6c118ded8ba31392563d19e490433e9a65382e707101",
        url="https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.002002.tar.gz",
    )
    version("1.001_001", sha256="4028af291bf39cadffd5aa4e03bb93c1c753b0beb545bba89c5920c6d20ca7fd")
    version(
        "1.000.000",
        sha256="ffdd77d57de099e8f64dd942ef12a00a3f4313c2531f342339eeed2d366ad078",
        url="https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.000000.tar.gz",
    )

    provides("perl-exporter-shiny")  # AUTO-CPAN2Spack
    depends_on("perl@5.6.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-warnings", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
