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


class Triangle(Package):
    """Triangle is a two-dimensional mesh generator and Delaunay
       triangulator. Triangle generates exact Delaunay triangulations,
       constrained Delaunay triangulations, conforming Delaunay
       triangulations, Voronoi diagrams, and high-quality triangular
       meshes."""

    homepage = "http://www.cs.cmu.edu/~quake/triangle.html"
    url      = "http://www.netlib.org/voronoi/triangle.zip"

    version('1.6', '10aff8d7950f5e0e2fb6dd2e340be2c9')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)

        install('triangle', prefix.bin)
        install('showme', prefix.bin)
