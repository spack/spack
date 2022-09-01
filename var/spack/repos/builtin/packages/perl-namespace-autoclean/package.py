# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNamespaceAutoclean(PerlPackage):
    """Keep imports out of your namespace."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/moose/namespace-autoclean"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/namespace-autoclean-0.29.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "0.30-TRIAL",
        sha256="4a19d87a72ebc2af5023b3b591d7ac8fd0b2a7daffbf8a70fab79bfe067f4a61",
        preferred=False,
    )
    version("0.29", sha256="45ebd8e64a54a86f88d8e01ae55212967c8aa8fed57e814085def7608ac65804")

    depends_on("perl-sub-identify", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-namespace-clean@0.20:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-b-hooks-endofscope@0.12:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack

