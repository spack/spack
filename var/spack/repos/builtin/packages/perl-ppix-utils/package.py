# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixUtils(PerlPackage):
    """Utility functions for PPI."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Grinnz/PPIx-Utils"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DB/DBOOK/PPIx-Utils-0.003.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.003", sha256="2a9bccfc8ead03be01b67248fe8e152522040f798286fa4ef4432b7f2efdba11")
    version("0.002", sha256="df9957cc4a15fa516579e1552b8508ced045c482b77d7fc8257b2115fa8b7c27")

    provides("perl-ppix-utils-classification")  # AUTO-CPAN2Spack
    provides("perl-ppix-utils-language")  # AUTO-CPAN2Spack
    provides("perl-ppix-utils-traversal")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-b-keywords@1.9:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-dumper", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-ppi@1.250:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack

