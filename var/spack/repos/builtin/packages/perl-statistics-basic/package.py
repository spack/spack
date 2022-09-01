# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStatisticsBasic(PerlPackage):
    """Statistics::Basic - A collection of very basic statistics modules"""

    homepage = "https://metacpan.org/pod/distribution/Statistics-Basic/lib/Statistics/Basic.pod"
    url = "https://cpan.metacpan.org/authors/id/J/JE/JETTERO/Statistics-Basic-1.6611.tar.gz"

    version(
        "1.66.11",
        sha256="6855ce5615fd3e1af4cfc451a9bf44ff29a3140b4e7130034f1f0af2511a94fb",
        url="https://cpan.metacpan.org/authors/id/J/JE/JETTERO/Statistics-Basic-1.6611.tar.gz",
    )
    version(
        "1.66.10",
        sha256="5823f96e61275b23b7e7e74b6e649a2d5e6c750bcbd0643b0dfc45ab6a7b353f",
        url="https://cpan.metacpan.org/authors/id/J/JE/JETTERO/Statistics-Basic-1.6610.tar.gz",
    )

    depends_on("perl-number-format", type=("build", "run"))
    depends_on("perl-scalar-list-utils", type=("build", "run"))
