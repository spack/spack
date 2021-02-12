# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlParallelForkmanager(PerlPackage):
    """A simple parallel processing fork manager"""

    homepage = "http://search.cpan.org/~yanick/Parallel-ForkManager/lib/Parallel/ForkManager.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Parallel-ForkManager-1.19.tar.gz"

    version('2.02', sha256='c1b2970a8bb666c3de7caac4a8f4dbcc043ab819bbc337692ec7bf27adae4404')
    version('1.20', sha256='7cc4c1c3b0e676b61ffa90f82f4128e8057327449ca86a9beb2f39217023f289')
    version('1.19', sha256='f1de2e9875eeb77d65f80338905dedd522f3913822502982f805aa71cde5a472')
