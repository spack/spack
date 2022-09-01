# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlContextualReturn(PerlPackage):
    """Create context-sensitive return values"""

    homepage = "https://metacpan.org/pod/Contextual::Return"
    url = "https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/Contextual-Return-0.004014.tar.gz"

    version(
        "0.004.014",
        sha256="09fe1415e16e49a69e13c0ef6e6a4a3fd8b856f389d3f3e624d7ab3b71719f78",
        url="https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/Contextual-Return-0.004014.tar.gz",
    )
    version(
        "0.004.012",
        sha256="1e6d3e802b12ba94488fb3c21ed9d2311b7bd1b6db7a6e5d5653300e2fb32543",
        url="https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/Contextual-Return-0.004012.tar.gz",
    )

    depends_on("perl-want")
