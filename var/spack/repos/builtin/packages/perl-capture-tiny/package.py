# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCaptureTiny(PerlPackage):
    """Capture STDOUT and STDERR from Perl, XS or external programs"""

    homepage = "https://metacpan.org/pod/Capture::Tiny"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Capture-Tiny-0.46.tar.gz"

    version("0.48", sha256="6c23113e87bad393308c90a207013e505f659274736638d8c79bac9c67cc3e19")
    version("0.46", sha256="5d7a6a830cf7f2b2960bf8b8afaac16a537ede64f3023827acea5bd24ca77015")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
