# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGraph(PerlPackage):
    """Graph data structures and algorithms"""

    homepage = "https://metacpan.org/pod/Graph"
    url = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Graph-0.9704.tar.gz"

    version("0.20105", sha256="d72d6512e5a637a64b879a7b74cf3822278b4917e1a0317d340523a6a3936b67")
    version("0.9704", sha256="325e8eb07be2d09a909e450c13d3a42dcb2a2e96cc3ac780fe4572a0d80b2a25")

    depends_on("perl@5.6.0:")
