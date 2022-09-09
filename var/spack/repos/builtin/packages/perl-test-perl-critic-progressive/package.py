# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestPerlCriticProgressive(PerlPackage):
    """Encourage Perl::Critic conformance over time."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TH/THALJEF/Test-Perl-Critic-Progressive-0.03.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.03", sha256="665d717b4a4c35077b703115090aaa64f24ae12c6193674c8a096f031bc15b36")
    version("0.02", sha256="be23f3d422aa02dff48fbb18201e8c1c48d7e32ec2e11020c4c069d39e857141")

    depends_on("perl-module-build", type="build")

    depends_on("perl-perl-critic-utils@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.82:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="run")  # AUTO-CPAN2Spack
