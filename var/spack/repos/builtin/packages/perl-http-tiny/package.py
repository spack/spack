# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpTiny(PerlPackage):
    """A small, simple, correct HTTP/1.1 client."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/chansen/p5-http-tiny"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/HTTP-Tiny-0.082.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.082", sha256="54e9e4a559a92cbb90e3f19c8a88ff067ec2f68fbe39bbb694ee70828cd5f4b8")

    depends_on("perl-http-cookiejar@0.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-socket-ip@0.32:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-mozilla-ca@20160104:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-local", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-net-ssleay@1.49:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-socket-ssl@1.42:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack

