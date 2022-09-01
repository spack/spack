# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTryTiny(PerlPackage):
    """Minimal try/catch with proper preservation of $@"""

    homepage = "https://metacpan.org/pod/Try::Tiny"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-0.28.tar.gz"

    version("0.31", sha256="3300d31d8a4075b26d8f46ce864a1d913e0e8467ceeba6655d5d2b2e206c11be")
    version("0.30", sha256="da5bd0d5c903519bbf10bb9ba0cb7bcac0563882bcfe4503aee3fb143eddef6b")
    version("0.29", sha256="d78ec3d97d1a92117c67be5aed4227121eba67b12eb175662469c153455b3f07")
    version("0.28", sha256="f1d166be8aa19942c4504c9111dade7aacb981bc5b3a2a5c5f6019646db8c146")
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
