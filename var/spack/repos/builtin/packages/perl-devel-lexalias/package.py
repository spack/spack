# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelLexalias(PerlPackage):
    """Alias lexical variables."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Devel-LexAlias-0.05.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.05", sha256="5e0ad9d43e266033856e424e104a0009f8e63449e40cd5aba59ad94cb1bcee72")
    version("0.04", sha256="f610bbabc530d3771192d9a2feb31c90dea891c1cc0bd5d3c5ccd1e324cd639c")

    depends_on("perl-devel-caller@0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
