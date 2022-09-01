# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlChi(PerlPackage):
    """Unified cache handling interface."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/A/AS/ASB"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AS/ASB/CHI-0.61.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.61", sha256="583545c9e5312bb4193ab16de9f55ff8f4b4a7ded128cee8dd2cb021d4678b5b")

    provides("perl-chi-cacheobject")  # AUTO-CPAN2Spack
    provides("perl-chi-driver")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-base-cachecontainer")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-cachecache")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-fastmmap")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-file")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-memory")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-metacache")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-null")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-rawmemory")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-role-hassubcaches")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-role-issizeaware")  # AUTO-CPAN2Spack
    provides("perl-chi-driver-role-issubcache")  # AUTO-CPAN2Spack
    provides("perl-chi-stats")  # AUTO-CPAN2Spack
    depends_on("perl-class-load", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-hash-moreutils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-hires@1.30:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-date-parse", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-task-weaken", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moox-types-mooselike-numeric", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moox-types-mooselike@0.23:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-log-any@0.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-warn", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-class", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-data-uuid", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-digest-md5", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils@0.13:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-mask", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-json-maybexs@1.3.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-carp-assert@0.20:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-duration@1.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moo@1.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moox-types-mooselike-base", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-duration-parse@0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-string-rewriteprefix", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-cache-filecache", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-exception", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-digest-jhash", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-try-tiny@0.5:", type="run")  # AUTO-CPAN2Spack

