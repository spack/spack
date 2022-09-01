# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleImplementation(PerlPackage):
    """Loads one of several alternate underlying implementations for a
    module"""

    homepage = "https://metacpan.org/pod/Module::Implementation"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Module-Implementation-0.09.tar.gz"

    version("0.09", sha256="c15f1a12f0c2130c9efff3c2e1afe5887b08ccd033bd132186d1e7d5087fd66d")

    depends_on("perl-test-fatal@0.6:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-requires", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-module-runtime@0.12:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-try-tiny", type="run")  # AUTO-CPAN2Spack
