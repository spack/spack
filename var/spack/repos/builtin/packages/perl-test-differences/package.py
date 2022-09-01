# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDifferences(PerlPackage):
    """Test strings and data structures and show differences if not ok"""

    homepage = "https://metacpan.org/pod/Test::Differences"
    url = "https://cpan.metacpan.org/authors/id/D/DC/DCANTRELL/Test-Differences-0.64.tar.gz"

    version("0.69", sha256="18f644fdd4a1fef93ef3f7f67df8e95b593d811899f34bcbbaba4d717222f58f")
    version("0.68", sha256="e68547206cb099a2594165ca0adc99fc12adb97c7f02a1222f62961fd775e270")
    version("0.67", sha256="c88dbbb48b934b069284874f33abbaaa438aa31204aa3fa73bfc2f4aeac878da")
    version("0.66", sha256="83633a171e83ff03a0eb1f5a699f05b506a34190bcf8726979bbfd9dc16c223a")
    version("0.65", sha256="83f4d1154b5638b01c0915559abc6adbc880631f1cd5d32d6214c1ee65315310")
    version("0.64", sha256="9f459dd9c2302a0a73e2f5528a0ce7d09d6766f073187ae2c69e603adf2eb276")

    depends_on("perl-module-build", type="build")
    depends_on("perl-text-diff@1.43:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-capture-tiny@0.24:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper@2.126:", type="run")  # AUTO-CPAN2Spack
