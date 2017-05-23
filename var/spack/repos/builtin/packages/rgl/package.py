##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Rgl(RPackage):
    """Provides medium to high level functions for 3D interactive graphics,
    including functions modelled on base graphics (plot3d(), etc.) as well as
    functions for constructing representations of geometric objects (cube3d(),
    etc.). Output may be on screen using OpenGL, or to various standard
    3D file formats including WebGL, PLY, OBJ, STL as well as 2D image formats,
    including PNG, Postscript, SVG, PGF.."""

    homepage = "https://r-forge.r-project.org/projects/rgl"
    url      = "https://cloud.r-project.org/src/contrib/rgl_0.98.1.tar.gz"

    list_url = 'https://cloud.r-project.org/src/contrib/Archive/rgl'

    version('0.98.1', 'bd69e1d33f1590feb4b6dc080b133e5b')

    depends_on('r@3.2:3.9')
    depends_on('zlib', type=('link'))
    depends_on('libpng', type=('link'))
    depends_on('freetype', type=('link'))
    depends_on('mesa', type=('link'))
    depends_on('mesa-glu', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
