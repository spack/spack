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


class Amrex(CMakePackage):
    """AMReX is the successor to BoxLib.
       It is a Block-Structured AMR Framework.
    """

    homepage = "https://ccse.lbl.gov/AMReX/index.html"
    url      = "https://github.com/AMReX-Codes/amrex.git"

    version('develop', git='https://github.com/AMReX-Codes/amrex.git', tag='master')
    version('17.06', git='https://github.com/AMReX-Codes/amrex.git', commit='836d3c7')

    variant('mpi', default=True, description='Enable MPI parallel support')
# variant('omp', default=False, description='Enable OpenMP parallel support')

    variant('dims',
        default='3',
        values=('1', '2', '3'),
        multi=False,
        description='Number of spatial dimensions')

    variant('prec',
        default='DOUBLE',
        values=('FLOAT', 'DOUBLE'),
        multi=False,
        description='Floating point precision')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('debug', default=False, description='Enable debugging features')
    variant('particles', default=False, description='Include particle classes in build')

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DENABLE_POSITION_INDEPENDENT_CODE=ON',
            '-DBL_SPACEDIM:INT=%d' % int(spec.variants['dims'].value),
            '-DBL_PRECISION:STRING=%s' % spec.variants['prec'].value,
        ]

        if '+fortran' in spec:
            cmake_args += [
                '-DENABLE_FMG=ON',
                '-DENABLE_FBASELIB=ON'
            ]

        if '+debug' not in spec:
            cmake_args += ['-DBL_DEBUG:INT=0']

        if '+particles' in spec:
            cmake_args += ['-DBL_USE_PARTICLES:INT=1']

        if '~mpi' in spec:
            cmake_args += ['-DENABLE_MPI:INT=0']
        else:
            cmake_args += [
                '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx
            ]
            if '+fortran' in spec:
                cmake_args += [
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
                ]
            else:
                cmake_args += ['-DENABLE_FORTRAN_MPI=OFF']

        return cmake_args
