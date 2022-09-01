# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestLeaktrace(PerlPackage):
    """Traces memory leaks."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Test-LeakTrace"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEEJO/Test-LeakTrace-0.17.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.17", sha256="777d64d2938f5ea586300eef97ef03eacb43d4c1853c9c3b1091eb3311467970")
    version("0.16", sha256="5f089eed915f1ec8c743f6d2777c3ecd0ca01df2f7b9e10038d316952583e403")

    provides("perl-test-leaktrace-script")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

