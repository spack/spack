# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigAutoconf(PerlPackage):
    """A module to implement some of AutoConf macros in pure perl."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Config-AutoConf"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AM/AMBS/Config-AutoConf-0.320.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.320", sha256="bb57a958ef49d3f7162276dae14a7bd5af43fd1d8513231af35d665459454023")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-file-slurper", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.18:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-capture-tiny", type="run")  # AUTO-CPAN2Spack
