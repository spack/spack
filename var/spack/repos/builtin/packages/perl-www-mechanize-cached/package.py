# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlWwwMechanizeCached(PerlPackage):
    """Cache response to be polite."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/libwww-perl/WWW-Mechanize-Cached"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/WWW-Mechanize-Cached-1.56.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.56", sha256="a18b0706aac202604adc575b6be6b8ae26b373a9d43d8da59c826d7d300151dd")
    version("1.55", sha256="3ab16463beede3061db7b7d3c66ea9536f02b737467cc6b1172aa08302d9fb60")

    depends_on("perl-test-warnings", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-data-dump", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-useragent@6.66:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-response", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-test-requiresinternet", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-path-tiny", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-uri-file", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-namespace-clean", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moo@1.4.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal", type="test")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type=("run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-moox-types-mooselike-base", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-cache-filecache", type=("run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-www-mechanize", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-runtime", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-chi", type=("run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-request", type="test")  # AUTO-CPAN2Spack
