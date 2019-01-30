# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
