# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestWarn(PerlPackage):
    """Perl extension to test methods for warnings"""

    homepage = "https://metacpan.org/pod/Test::Warn"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHORNY/Test-Warn-0.30.tar.gz"

    version("0.30", sha256="8197555b94189d919349a03f7058f83861f145af9bee59f505bfe47562144e41")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-sub-uplevel@0.12:", type="run")  # AUTO-CPAN2Spack
