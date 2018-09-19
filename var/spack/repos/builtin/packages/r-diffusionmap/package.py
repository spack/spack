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


class RDiffusionmap(RPackage):
    """Allows to display a progress bar in the R console for long running
    computations taking place in c++ code, and support for interrupting those
    computations even in multithreaded code, typically using OpenMP."""

    homepage = "https://cran.r-project.org/web/packages/diffusionMap/index.html"
    url      = "https://cran.r-project.org/src/contrib/diffusionMap_1.1-0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/diffusionMap"

    version('1.1-0', 'cc7d728087ba08d9299ae3a64a8d8919')
    version('1.0-0', 'bca462e6efe45c5eaa48d38621f0bd6f')
    version('0.0-2', 'b599f47ebf30127e34ce2219dc3e43ae')
    version('0.0-1', '20c2cc2fffb5237d5c0216207016c2a1')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
