# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSpiffy(PerlPackage):
    """Spiffy Perl Interface Framework For You."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/ingydotnet/spiffy-pm"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/I/IN/INGY/Spiffy-0.46.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.46", sha256="8f58620a8420255c49b6c43c5ff5802bd25e4f09240c51e5bf2b022833d41da3")
    version("0.45", sha256="28858d63ceed43566da4eea61175ed51de8ecbe5f72f698389d5647340ca2f14")

    provides("perl-spiffy-mixin")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.30:", type="build")  # AUTO-CPAN2Spack

