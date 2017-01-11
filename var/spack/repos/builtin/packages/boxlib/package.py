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


class Boxlib(CMakePackage):
    """BoxLib, a software framework for massively parallel
       block-structured adaptive mesh refinement (AMR) codes."""

    homepage = "https://ccse.lbl.gov/BoxLib/"
    base_url = "https://github.com/BoxLib-Codes/BoxLib.git"

    version('master', git='https://github.com/BoxLib-Codes/BoxLib.git',
            tag='master')

    # Latest version has build errors when using CMake
    # version('1.3.5', '78f9436e152f18d0e55f6fd9b4e35a33',
    #     tag='v1.3.5', git='https://github.com/BoxLib-Codes/BoxLib.git')

    depends_on('mpi')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            # '-DBL_SPACEDIM=3',
            '-DENABLE_POSITION_INDEPENDENT_CODE=ON',
            '-DENABLE_FBASELIB=ON',
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].prefix.bin + "/mpicc",
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].prefix.bin + "/mpic++",
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].prefix.bin + "/mpif90"
        ])

        return options
