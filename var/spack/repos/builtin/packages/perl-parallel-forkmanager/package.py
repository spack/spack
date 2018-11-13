# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlParallelForkmanager(PerlPackage):
    """A simple parallel processing fork manager"""

    homepage = "http://search.cpan.org/~yanick/Parallel-ForkManager/lib/Parallel/ForkManager.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Parallel-ForkManager-1.19.tar.gz"

    version('1.19', '0e7137dd4b6948e1633b3b9ebe3b87e1')
