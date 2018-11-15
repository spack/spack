# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGraph(PerlPackage):
    """Graph data structures and algorithms"""

    homepage = "http://search.cpan.org/~jhi/Graph/lib/Graph.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Graph-0.9704.tar.gz"

    version('0.9704', '1ab4e49420e56eeb1bc81d842aa8f3af')

    depends_on('perl@5.6.0:')
