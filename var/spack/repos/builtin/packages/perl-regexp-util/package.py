# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRegexpUtil(PerlPackage):
    """A selection of general-utility regexp subroutines."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Regexp-Util"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Regexp-Util-0.005.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.005", sha256="a08871fca2054c464ec6cd663fbdb2fce99cc0346256acf0a4936681ed8a0e00")
    version("0.004", sha256="21f34ef3d445c20695ae35302167cc1db709ac697591eb17140635400c8901ee")

    depends_on("perl@5.10:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-exporter-tiny", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack

