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


class Cleverleaf(Package):
    """CleverLeaf is a hydrodynamics mini-app that extends CloverLeaf with
       Adaptive Mesh Refinement using the SAMRAI toolkit from Lawrence
       Livermore National Laboratory. The primary goal of CleverLeaf is
       to evaluate the application of AMR to the Lagrangian-Eulerian
       hydrodynamics scheme used by CloverLeaf.

    """

    homepage = "http://uk-mac.github.io/CleverLeaf/"
    url      = "https://github.com/UK-MAC/CleverLeaf/tarball/master"

    version('develop', git='https://github.com/UK-MAC/CleverLeaf_ref.git',
            branch='develop')

    depends_on("samrai@3.8.0:")
    depends_on("hdf5+mpi")
    depends_on("boost")
    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        cmake(*std_cmake_args)
        make()
        make("install")
