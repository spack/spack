# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTaskWeaken(PerlPackage):
    """Ensure that a platform has weaken support"""

    homepage = "https://metacpan.org/pod/Task::Weaken"
    url = "https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Task-Weaken-1.04.tar.gz"

    version("1.04", sha256="67e271c55900fe7889584f911daa946e177bb60c8af44c32f4584b87766af3c4")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type=("build", "test"))  # AUTO-CPAN2Spack

    def setup_build_environment(self, env):
        env.prepend_path("PERL5LIB", self.stage.source_path)
