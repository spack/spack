# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTaskPerlCritic(PerlPackage):
    """Install everything Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TH/THALJEF/Task-Perl-Critic-1.008.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.008", sha256="626e4d746023b1f573f05a90fdcd0a0eb8f1b292882ac6535cadbdcd281f16ce")

    depends_on("perl-module-build", type="build")

    depends_on("perl-perl-critic-pulp@3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-perl-critic-progressive@0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-itch", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-strictersubs@0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-petpeeves-jtrammell@0.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-lax@0.7:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-nits@1.0.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-criticism@1.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-dynamic@0.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-compatibility@1.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-tics@0.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-storable", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-perl-critic@1.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-swift@1.0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.117:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.38:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-moose", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-bangs@1.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-more@1.0:", type="run")  # AUTO-CPAN2Spack
