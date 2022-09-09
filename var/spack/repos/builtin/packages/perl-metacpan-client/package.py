# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMetacpanClient(PerlPackage):
    """A comprehensive, DWIM-featured client to the MetaCPAN API."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/MI/MICKEY"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/MI/MICKEY/MetaCPAN-Client-2.030000.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "2.030.000",
        sha256="d9b765c5237754f17262696382a7385d90b2d01986979817862b1664b06dd3af",
        url="https://cpan.metacpan.org/authors/id/M/MI/MICKEY/MetaCPAN-Client-2.030000.tar.gz",
    )
    version(
        "2.029.000",
        sha256="c5d883903b379a5a6adb02e016ec5b52288af05652d564c895316593f3c7e57c",
        url="https://cpan.metacpan.org/authors/id/M/MI/MICKEY/MetaCPAN-Client-2.029000.tar.gz",
    )

    provides("perl-metacpan-client-author")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-cover")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-distribution")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-downloadurl")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-favorite")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-file")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-mirror")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-module")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-package")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-permission")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-pod")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-rating")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-release")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-request")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-resultset")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-role-entity")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-role-hasua")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-scroll")  # AUTO-CPAN2Spack
    provides("perl-metacpan-client-types")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@7.11_1:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-http-tiny-mech@1.1.2:", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-http-tiny@0.56:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-socket-ssl@1.42:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-json-maybexs", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-protocol-https", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-moo", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-moo-role", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-net-ssleay@1.49:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ref-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-safe-isa", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-test-needs@0.2.5:", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-type-tiny", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri-escape", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-www-mechanize-cached@1.54:", type="test")  # AUTO-CPAN2Spack
    depends_on("perl@5.10:", type="run")  # AUTO-CPAN2Spack
