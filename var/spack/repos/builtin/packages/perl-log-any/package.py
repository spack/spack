# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLogAny(PerlPackage):
    """Bringing loggers and listeners together."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/preaction/Log-Any"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PR/PREACTION/Log-Any-1.710.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.710", sha256="bdb65fd0a8888fd4522f39f0fe95e94cb9267ef1fd9f7737564d46527b306f6f")
    version("1.709", sha256="80e4b00f494f365082650222b228d2925b37ed7efaf94052087c68b2f4291e85")

    provides("perl-log-any-adapter")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-base")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-capture")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-file")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-multiplex")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-null")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-stderr")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-stdout")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-syslog")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-test")  # AUTO-CPAN2Spack
    provides("perl-log-any-adapter-util")  # AUTO-CPAN2Spack
    provides("perl-log-any-manager")  # AUTO-CPAN2Spack
    provides("perl-log-any-proxy")  # AUTO-CPAN2Spack
    provides("perl-log-any-proxy-null")  # AUTO-CPAN2Spack
    provides("perl-log-any-proxy-test")  # AUTO-CPAN2Spack
    provides("perl-log-any-test")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
