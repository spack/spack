# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RParallelmap(RPackage):
    """Unified parallelization framework for multiple back-end, designed for
       internal package and interactive usage. The main operation is a parallel
       "map" over lists. Supports local, multicore, mpi and BatchJobs mode.
       Allows "tagging" of the parallel operation with a level name that can be
       later selected by the user to switch on parallel execution for exactly
       this operation."""

    homepage = "https://github.com/berndbischl/parallelMap"
    url      = "https://cran.r-project.org/src/contrib/parallelMap_1.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/parallelMap"

    version('1.3', 'dd62866b395847b0bd5b13bed98c0081')

    depends_on('r-bbmisc@1.8:', type=('build', 'run'))
    depends_on('r-checkmate@1.5.1:', type=('build', 'run'))
