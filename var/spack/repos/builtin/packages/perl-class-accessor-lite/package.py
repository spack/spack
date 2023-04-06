# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassAccessorLite(PerlPackage):
    """A minimalistic variant of Class::Accessor."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/K/KA/KAZUHO"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZUHO/Class-Accessor-Lite-0.08.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.08", sha256="75b3b8ec8efe687677b63f0a10eef966e01f60735c56656ce75cbb44caba335a")
    version("0.07", sha256="a8aaaaf32a64e9ff89dbc4ef8a55d6197f5c161b8fc8d64219eef9ea173971d1")

    depends_on("perl-extutils-makemaker@6.36:", type="build")  # AUTO-CPAN2Spack

    def setup_build_environment(self, env):
        env.prepend_path("PERL5LIB", self.stage.source_path)
