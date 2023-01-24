# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleCorelist(PerlPackage):
    """Module::CoreList - what modules shipped with versions of perl"""

    homepage = "https://metacpan.org/pod/Module::CoreList"
    url = "https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-CoreList-5.20220820.tar.gz"

    version(
        "5.20220820", sha256="708effbbf04158b087d34d8acc707f35bdab9dccc61b41d432cb6d995d137f43"
    )
