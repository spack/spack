# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGraph(PerlPackage):
    """Graph data structures and algorithms"""

    homepage = "http://search.cpan.org/~jhi/Graph/lib/Graph.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Graph-0.9704.tar.gz"

    version('0.20105', sha256='d72d6512e5a637a64b879a7b74cf3822278b4917e1a0317d340523a6a3936b67')
    version('0.20104', sha256='1c04528d07aefe45a897583456609ebfd9f6940017a971dc4acc585c71c0c5de')
    version('0.20103', sha256='14deba19ae25ffcf5d4de747c58f29b309be80f8526dd807c53b685c9d101ceb')
    version('0.20102', sha256='83cbf9f98e1547e149a35c9ae3e886f0c9e6a2e2ecc678724e21f94c1d652e89')
    version('0.20101', sha256='f8a748201c134e715e3c379273aeef214dd3a8e6920723f94f0d37ab72321aec')
    version('0.9704', sha256='325e8eb07be2d09a909e450c13d3a42dcb2a2e96cc3ac780fe4572a0d80b2a25')

    depends_on('perl@5.6.0:')
