# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetHttp(PerlPackage):
    """Low-level HTTP connection (client)"""

    homepage = "https://metacpan.org/pod/Net::HTTP"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/Net-HTTP-6.17.tar.gz"

    version("6.22", sha256="62faf9a5b84235443fe18f780e69cecf057dea3de271d7d8a0ba72724458a1a2")
    version("6.21", sha256="375aa35b76be99f06464089174d66ac76f78ce83a5c92a907bbfab18b099eec4")
    version("6.20", sha256="92527b2a24512961b8e3637c6216a057751e39b6fa751422ed181ff599779f1e")
    version("6.19", sha256="52b76ec13959522cae64d965f15da3d99dcb445eddd85d2ce4e4f4df385b2fc4")
    version("6.18", sha256="7e42df2db7adce3e0eb4f78b88c450f453f5380f120fd5411232e03374ba951c")
    version("6.17", sha256="1e8624b1618dc6f7f605f5545643ebb9b833930f4d7485d4124aa2f2f26d1611")

    provides("perl-net-http-methods")  # AUTO-CPAN2Spack
    provides("perl-net-http-nb")  # AUTO-CPAN2Spack
    provides("perl-net-https")  # AUTO-CPAN2Spack
    depends_on("perl@5.6.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-uncompress-gunzip", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-compress-raw-zlib", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack
