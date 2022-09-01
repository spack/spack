# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoSocketIp(PerlPackage):
    """Family-neutral IP socket supporting both IPv4 and IPv6."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS/IO-Socket-IP-0.41.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.41", sha256="849a45a238f8392588b97722c850382c4e6d157cd08a822ddcb9073c73bf1446")
    version("0.40", sha256="db50cc58f02c63edec35ecfd27818312fdb6e3de6ba7de338197500e26b9fa30")

    depends_on("perl-module-build", type="build")

    depends_on("perl-module-build@0.40.4:", type="build")  # AUTO-CPAN2Spack

