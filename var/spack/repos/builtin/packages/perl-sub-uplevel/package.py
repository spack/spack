# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubUplevel(PerlPackage):
    """apparently run a function in a higher stack frame"""

    homepage = "https://metacpan.org/pod/Sub::Uplevel"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Sub-Uplevel-0.2800.tar.gz"

    version("0.28.00", sha256="b4f3f63b80f680a421332d8851ddbe5a8e72fcaa74d5d1d98f3c8cc4a3ece293")
    version("0.26.00", sha256="e833e29b7d6037efee6d7ee2056cbb8aaaa908e4f5451969043093eb2917a166")
    version("0.25", sha256="2dcca582a7ea5bada576eb27c4be1d1b064fb22175bdbd6d696c45d083560505")
    version("0.24", sha256="0f93f6e9c80b8dcb22c60d0e9df2c2c6d7db10d4d37151f1dfea6e54a3c6fdfb")
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
