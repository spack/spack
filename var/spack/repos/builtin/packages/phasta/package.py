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


class Phasta(CMakePackage):
    """SCOREC RPI's Parallel Hierarchic Adaptive Stabilized Transient Analysis
       (PHASTA) of compressible and incompressible Navier Stokes equations."""

    homepage = "https://www.scorec.rpi.edu/software.php"
    git      = "https://github.com/PHASTA/phasta.git"

    version('develop', branch='master')
    version('0.0.1', commit='11f431f2d1a53a529dab4b0f079ab8aab7ca1109')

    depends_on('mpi')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DPHASTA_USE_MPI=ON',
            '-DPHASTA_BUILD_CONVERTERIO=OFF',
            '-DPHASTA_BUILD_ACUSTAT=OFF',
            '-DPHASTA_BUILD_M2N=OFF',
            '-DPHASTA_BUILD_M2NFixBnd=OFF',
            '-DPHASTA_USE_LESLIB=OFF',
            '-DPHASTA_USE_PETSC=OFF',
            '-DPHASTA_USE_SVLS=ON',
            '-DPHASTA_INCOMPRESSIBLE=ON',
            '-DPHASTA_COMPRESSIBLE=ON',
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
        ]

        return args
