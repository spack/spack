# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpl(CMakePackage):
    """A C++17 message passing library based on MPI."""

    homepage    = "https://rabauke.github.io/mpl/html/"
    git         = "https://github.com/rabauke/mpl.git"
    url         = "https://github.com/rabauke/mpl/archive/refs/tags/v0.1.tar.gz"
    maintainers = ['rabauke']

    version('develop', branch='master')
    version('0.1', tag='v0.1')

    depends_on('mpi')
