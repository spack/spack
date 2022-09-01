# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFontAfm(PerlPackage):
    """Interface to Adobe Font Metrics files."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/G/GA/GAAS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/G/GA/GAAS/Font-AFM-1.20.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.20", sha256="32671166da32596a0f6baacd0c1233825a60acaf25805d79c81a3f18d6088bc1")
    version("1.19", sha256="6b77e90b8922e899ed75bb77b779f6aba3870736f1edd553e94cb219c7bf02a0")

    provides("perl-font-metrics-courier")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-courierbold")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-courierboldoblique")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-courieroblique")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-helvetica")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-helveticabold")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-helveticaboldoblique")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-helveticaoblique")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-timesbold")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-timesbolditalic")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-timesitalic")  # AUTO-CPAN2Spack
    provides("perl-font-metrics-timesroman")  # AUTO-CPAN2Spack

