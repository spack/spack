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


class Tethex(Package):
    """Tethex is designed to convert triangular (in 2D) or tetrahedral (in 3D)
    Gmsh's mesh to quadrilateral or hexahedral one respectively. These meshes
    can be used in software packages working with hexahedrals only - for
    example, deal.II.
    """

    homepage = "https://github.com/martemyev/tethex"
    url      = "https://github.com/martemyev/tethex/archive/v0.0.7.tar.gz"

    version('0.0.7', '6c9e4a18a6637deb4400c6d77ec03184')
    version('develop', git='https://github.com/martemyev/tethex.git')

    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        cmake('.')
        make()

        # install by hand
        mkdirp(prefix.bin)
        install('tethex', prefix.bin)
