# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubName(PerlPackage):
    """Name or rename a sub"""

    homepage = "https://metacpan.org/pod/Sub::Name"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Sub-Name-0.21.tar.gz"

    version("0.21", sha256="bd32e9dee07047c10ae474c9f17d458b6e9885a6db69474c7a494ccc34c27117")
