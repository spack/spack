# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpCookiejar(PerlPackage):
    """A minimalist HTTP user agent cookie jar."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/dagolden/HTTP-CookieJar"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/HTTP-CookieJar-0.014.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.014", sha256="7094ea5c91f536d263b85e83ab4e9a963e11c4408ce08ecae553fa9c0cc47e73")

    provides("perl-http-cookiejar-lwp")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-time-local@1.19.1:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-uri", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-requires", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-date", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-mozilla-publicsuffix", type="run")  # AUTO-CPAN2Spack
