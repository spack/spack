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


class Tetgen(Package):
    """TetGen is a program and library that can be used to generate
       tetrahedral meshes for given 3D polyhedral domains. TetGen
       generates exact constrained Delaunay tetrahedralizations,
       boundary conforming Delaunay meshes, and Voronoi paritions.
    """

    homepage = "http://www.tetgen.org"
    url      = "http://www.tetgen.org/files/tetgen1.4.3.tar.gz"

    version('1.4.3', 'd6a4bcdde2ac804f7ec66c29dcb63c18')
    version('1.5.0', '3b9fd9cdec121e52527b0308f7aad5c1', url='http://www.tetgen.org/1.5/src/tetgen1.5.0.tar.gz')

    # TODO: Make this a build dependency once build dependencies are supported
    # (see: https://github.com/LLNL/spack/pull/378).
    depends_on('cmake@2.8.7:', when='@1.5.0:')

    def install(self, spec, prefix):
        make('tetgen', 'tetlib')

        mkdirp(prefix.bin)
        install('tetgen', prefix.bin)

        mkdirp(prefix.include)
        install('tetgen.h', prefix.include)

        mkdirp(prefix.lib)
        install('libtet.a', prefix.lib)
