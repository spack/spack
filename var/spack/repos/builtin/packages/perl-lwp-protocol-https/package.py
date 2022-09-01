# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLwpProtocolHttps(PerlPackage):
    """Provide https support for LWP::UserAgent"""

    homepage = "https://metacpan.org/pod/LWP::Protocol::https"
    url = "http://cpan.metacpan.org/authors/id/G/GA/GAAS/LWP-Protocol-https-6.04.tar.gz"

    version("6.04", sha256="1ef67750ee363525cf729b59afde805ac4dc80eaf8d36ca01082a4d78a7af629")
    version("6.03", sha256="cb864de7677cc3fc9f8f4aaa17c2984d970fdfa46fc7e3cb90bc5ef2c3e3c6f1")

    provides("perl-lwp-protocol-https-socket")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-net-https@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-useragent@6.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-mozilla-ca@20180117:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-socket-ssl-utils", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-socket-ssl@1.54:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-requiresinternet", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-lwp-protocol-http", type="run")  # AUTO-CPAN2Spack
