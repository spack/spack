# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataOptlist(PerlPackage):
    """Parse and validate simple name/value option pairs"""

    homepage = "https://metacpan.org/pod/Data::OptList"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Data-OptList-0.110.tar.gz"

    version("0.112", sha256="62c60ccaae88d5339ae36bcc8940b03388cf84adbf27828b1f8b300307103bab")
    version("0.110", sha256="366117cb2966473f2559f2f4575ff6ae69e84c69a0f30a0773e1b51a457ef5c3")

    depends_on("perl-params-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-install@0.921:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.78:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
