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


class RDeldir(RPackage):
    """Calculates the Delaunay triangulation and the Dirichlet or Voronoi
    tessellation (with respect to the entire plane) of a planar point set.
    Plots triangulations and tessellations in various ways. Clips
    tessellations to sub-windows. Calculates perimeters of tessellations.
    Summarises information about the tiles of the tessellation."""

    homepage = "https://CRAN.R-project.org/package=deldir"
    url      = "https://cran.r-project.org/src/contrib/deldir_0.1-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/deldir"

    version('0.1-14', '6a22b13d962615cd9d51b6eae403409f')

    depends_on('r@0.99:')
