# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestRequires(PerlPackage):
    """Checks to see if the module can be loaded."""

    homepage = "https://metacpan.org/pod/Test::Requires"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOKUHIROM/Test-Requires-0.10.tar.gz"

    version("0.11", sha256="4b88de549597eecddf7c3c38a4d0204a16f59ad804577b671896ac04e24e040f")
    version("0.10", sha256="2768a391d50ab94b95cefe540b9232d7046c13ee86d01859e04c044903222eb5")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.64:", type="build")  # AUTO-CPAN2Spack
