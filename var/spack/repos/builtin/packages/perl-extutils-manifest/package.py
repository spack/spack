# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsManifest(PerlPackage):
    """Utilities to write and check a MANIFEST file."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/ExtUtils-Manifest"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/ExtUtils-Manifest-1.73.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.73", sha256="dc5c063dac0b1ad64fa43cda3a51ee66e1952be8da495ddb34b82f9db88fbaf8")
    version("1.72", sha256="799280074f98ef2d7fdf4f75521ad83ec01c2e068e54a45c92968cd9dc2db45e")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack

