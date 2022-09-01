# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFilePathlist(PerlPackage):
    """Find a file within a set of paths (like @INC or Java classpaths)."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/A/AD/ADAMK"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AD/ADAMK/File-PathList-1.04.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.04", sha256="e3e2799f3bceeae4992fe31ea892c34e9141f9237598cfadbc89824ede7a662c")
    version("0.03", sha256="468c89cac5629092a3665378c89ed6f9363dbe046c537fc98d4837c221b6f80b")

    depends_on("perl@5.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-install", type="build")
    depends_on("perl-params-util@0.24:", type="run")  # AUTO-CPAN2Spack


    def setup_build_environment(self, env):
        env.prepend_path("PERL5LIB", self.stage.source_path)
