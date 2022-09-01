# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataDump(PerlPackage):
    """Pretty printing of data structures."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/G/GA/GARU"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/G/GA/GARU/Data-Dump-1.25.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.25", sha256="a4aa6e0ddbf39d5ad49bddfe0f89d9da864e3bc00f627125d1bc580472f53fbd")
    version("1.24", sha256="cc0275545125ee6ab985fe1e844c3723b0b137b8bb727e8834362ef5cd6d9d1a")

    provides("perl-data-dump-filtercontext")  # AUTO-CPAN2Spack
    provides("perl-data-dump-filtered")  # AUTO-CPAN2Spack
    provides("perl-data-dump-trace@0.02")  # AUTO-CPAN2Spack
    provides("perl-data-dump-trace-call")  # AUTO-CPAN2Spack
    provides("perl-data-dump-trace-wrapper")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

