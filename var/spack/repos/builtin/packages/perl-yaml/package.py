# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYaml(PerlPackage):
    """This module has been released to CPAN as YAML::Old, and soon YAML.pm
    will be changed to just be a frontend interface module for all the
    various Perl YAML implementation modules, including YAML::Old"""

    homepage = "https://metacpan.org/pod/YAML"
    url = "https://cpan.metacpan.org/authors/id/T/TI/TINITA/YAML-1.27.tar.gz"

    version("1.27", sha256="c992a1e820de0721b62b22521de92cdbf49edc306ab804c485b4b1ec25f682f9")
    provides("perl-yaml-any")  # AUTO-CPAN2Spack
    provides("perl-yaml-dumper")  # AUTO-CPAN2Spack
    provides("perl-yaml-dumper-base")  # AUTO-CPAN2Spack
    provides("perl-yaml-error")  # AUTO-CPAN2Spack
    provides("perl-yaml-loader")  # AUTO-CPAN2Spack
    provides("perl-yaml-loader-base")  # AUTO-CPAN2Spack
    provides("perl-yaml-marshall")  # AUTO-CPAN2Spack
    provides("perl-yaml-mo")  # AUTO-CPAN2Spack
    provides("perl-yaml-node")  # AUTO-CPAN2Spack
    provides("perl-yaml-tag")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-blessed")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-code")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-glob")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-ref")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-regexp")  # AUTO-CPAN2Spack
    provides("perl-yaml-type-undef")  # AUTO-CPAN2Spack
    provides("perl-yaml-types")  # AUTO-CPAN2Spack
    provides("perl-yaml-warning")  # AUTO-CPAN2Spack
    provides("perl-yaml-mapping")  # AUTO-CPAN2Spack
    provides("perl-yaml-scalar")  # AUTO-CPAN2Spack
    provides("perl-yaml-sequence")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-yaml@1.5:", type=("build", "test"))  # AUTO-CPAN2Spack
