# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCpanMetaYaml(PerlPackage):
    """Read and write a subset of YAML for CPAN Meta files."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Perl-Toolchain-Gang/CPAN-Meta-YAML"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/CPAN-Meta-YAML-0.018.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.018", sha256="33caf7c94cde58abdbd370a5ae7149635d4085c643d4838aa0ada97568821294")

    depends_on("perl@5.8.1:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
