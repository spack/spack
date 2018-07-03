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


class Amrex(CMakePackage):
    """AMReX is the successor to BoxLib.
       It is a Block-Structured AMR Framework.
    """

    homepage = "https://ccse.lbl.gov/AMReX/index.html"
    url      = "https://github.com/AMReX-Codes/amrex.git"

    version('17.06', git='https://github.com/AMReX-Codes/amrex.git', commit='836d3c7')
    version('master', git='https://github.com/AMReX-Codes/amrex.git', tag='master')
    version('develop', git='https://github.com/AMReX-Codes/amrex.git', tag='development')

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

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('openmp', default=False, description='Enable OpenMP parallel support')
    variant('fortran', default=True, description='Enable Fortran support')
    variant('debug', default=False, description='Enable debugging features')
    variant('particles', default=False, description='Include particle classes in build')

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON',
            '-DBL_SPACEDIM:INT=%d' % int(spec.variants['dims'].value),
            '-DBL_PRECISION:STRING=%s' % spec.variants['prec'].value,
            '-DENABLE_FMG=%s' % ('+fortran' in spec),
            '-DENABLE_FBASELIB=%s' % ('+fortran' in spec),
            '-DBL_DEBUG:INT=%d' % int('+debug' in spec),
            '-DBL_USE_PARTICLES:INT=%d' % int('+particles' in spec),
            '-DENABLE_MPI:INT=%d' % int('+mpi' in spec),
            '-DENABLE_OpenMP:INT=%d' % int('+openmp' in spec),
        ]

        if '+mpi' in spec:
            cmake_args += [
                '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx
            ]
            if '+fortran' in spec:
                cmake_args += [
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
                ]
            cmake_args += ['-DENABLE_FORTRAN_MPI=%s' % ('+fortran' in spec)]

        return cmake_args
