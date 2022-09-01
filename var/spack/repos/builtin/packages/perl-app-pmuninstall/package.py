# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAppPmuninstall(PerlPackage):
    """Uninstall modules."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/xaicron/pm-uninstall"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/X/XA/XAICRON/App-pmuninstall-0.33.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.33", sha256="f05a12435124046a2a45bce49f283216797e71fe1b129bcf43b3f04887c89aff")
    version("0.32", sha256="ebc4f6cb4c9fd9ceee0d2d83b1d54d61fd2ccb43a624a86fcc6dcd51e922132d")

    depends_on("perl-module-build", type="build")

    depends_on("perl-yaml", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-cpan-distnameinfo", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build-tiny@0.35:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-module-corelist", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-tiny@0.12:", type="run")  # AUTO-CPAN2Spack

