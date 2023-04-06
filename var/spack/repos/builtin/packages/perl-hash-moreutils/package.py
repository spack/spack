# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHashMoreutils(PerlPackage):
    """Provide the stuff missing in Hash::Util."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/Hash-MoreUtils"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Hash-MoreUtils-0.06.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.06", sha256="db9a8fb867d50753c380889a5e54075651b5e08c9b3b721cb7220c0883547de8")
    version("0.05", sha256="5e9c8458457eb18315a5669e3bef68488cd5ed8c2220011ac7429ff983288ab1")

    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
