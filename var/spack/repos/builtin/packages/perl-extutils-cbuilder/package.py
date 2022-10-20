# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsCbuilder(PerlPackage):
    """Compile and link C code for Perl modules."""  # AUTO-CPAN2Spack

    homepage = "http://search.cpan.org/dist/ExtUtils-CBuilder"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AM/AMBS/ExtUtils-CBuilder-0.280236.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "0.28.2.36",
        url="https://cpan.metacpan.org/authors/id/A/AM/AMBS/ExtUtils-CBuilder-0.280236.tar.gz",
        sha256="abc21827eb8a513171bf7fdecefce9945132cb76db945036518291f607b1491f",
    )
    version(
        "0.28.2.35",
        url="https://cpan.metacpan.org/authors/id/A/AM/AMBS/ExtUtils-CBuilder-0.280235.tar.gz",
        sha256="a0f454d84eb599bf0c11b976ab2ce39ada49bf84c323c7a53fe9f8941ee9378a",
    )

    provides("perl-extutils-cbuilder-base")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-unix")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-vms")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-windows")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-windows-bcc")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-windows-gcc")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-windows-msvc")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-aix")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-android")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-cygwin")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-darwin")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-dec-osf")  # AUTO-CPAN2Spack
    provides("perl-extutils-cbuilder-platform-os2")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.30:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-ostype@1:", type="run")  # AUTO-CPAN2Spack
