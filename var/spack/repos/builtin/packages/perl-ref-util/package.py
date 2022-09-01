# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRefUtil(PerlPackage):
    """Utility functions for checking references."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/A/AR/ARC"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARC/Ref-Util-0.204.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.204", sha256="415fa73dbacf44f3d5d79c14888cc994562720ab468e6f71f91cd1f769f105e1")
    version("0.203", sha256="6425ffd7ec0c1799086daf5b4e848211ca5d058bd75b7629dbab7b739dfb6dfb")

    provides("perl-ref-util-pp")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack

