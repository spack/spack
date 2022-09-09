# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestLongstring(PerlPackage):
    """Tests strings for equality, with more helpful failures."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RG/RGARCIA"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Test-LongString-0.17.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.17", sha256="abc4349eaf04d1bec1e464166a3018591ea846d8f3c5c9c8af4ac4905d3e974f")
    version("0.16", sha256="2140532559280f0e0f19b4af1b9e5c1834835521fa39bc79e4e409b84daa49aa")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
