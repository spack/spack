##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
