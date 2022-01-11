# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scorpio(CMakePackage):
    """SCORPIO Scalable Parallel I/O module for Environmental Management Applications

    This library provides software that read/write data sets from/to parallel file
    systems in an efficient and scalable manner
    """

    homepage = "https://gitlab.com/truchas/tpl-forks/scorpio"
    git      = "https://gitlab.com/truchas/tpl-forks/scorpio.git"

    maintainers = ['pbrady']

    version('develop', branch='truchas')

    version('2021-12-10',
            commit='b802f16877a6562ccdbeca8887910d3bd3e25cbb',
            preferred=True)

    depends_on('cmake@3.16:', type='build')
    depends_on('mpi')
    depends_on('hdf5@1.10.6: +hl +mpi')
