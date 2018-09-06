##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Vpic(CMakePackage):
    """VPIC is a general purpose particle-in-cell simulation code for modeling
       kinetic plasmas in one, two, or three spatial dimensions. It employs a
       second-order, explicit, leapfrog algorithm to update charged particle
       positions and velocities in order to solve the relativistic kinetic
       equation for each species in the plasma, along with a full Maxwell
       description for the electric and magnetic fields evolved via a second-
       order finite-difference-time-domain (FDTD) solve.
    """
    homepage = "https://github.com/lanl/vpic"
    git      = "https://github.com/lanl/vpic.git"

    version('develop', branch='master', submodules=True)

    depends_on("cmake@3.1:", type='build')
    depends_on('mpi')

    def cmake_args(self):
        options = ['-DENABLE_INTEGRATED_TESTS=ON', '-DENABLE_UNIT_TESTS=ON']

        return options
