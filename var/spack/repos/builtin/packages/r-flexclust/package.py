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


class RFlexclust(RPackage):
    """The main function kcca implements a general framework for k-centroids
    cluster analysis supporting arbitrary distance measures and centroid
    computation. Further cluster methods include hard competitive learning,
    neural gas, and QT clustering. There are numerous visualization methods for
    cluster results (neighborhood graphs, convex cluster hulls, barcharts of
    centroids, ...), and bootstrap methods for the analysis of cluster
    stability."""

    homepage = "https://cran.r-project.org/package=flexclust"
    url      = "https://cran.rstudio.com/src/contrib/flexclust_1.3-5.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/flexclust"

    version('1.3-5', '90226a0e3a4f256f392a278e9543f8f4')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-modeltools', type=('build', 'run'))
