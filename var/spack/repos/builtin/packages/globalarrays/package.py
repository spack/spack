##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at IBM.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@ibm.com, All rights reserved.
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


class Globalarrays(CMakePackage):
    """The Global Arrays (GA) toolkit provides a shared memory style
    programming environment in the context of distributed array data
    structures.
    """

    homepage = "http://hpc.pnl.gov/globalarrays/"
    url = "https://github.com/GlobalArrays/ga"

    version('master', git='https://github.com/GlobalArrays/ga', branch='master')

    variant('i8', default=False, description='Build with 8 byte integers')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')

    patch('ibm-xl.patch', when='%xl')
    patch('ibm-xl.patch', when='%xl_r')

    def cmake_args(self):
        options = []

        options.extend([
            '-DENABLE_FORTRAN=ON',
            '-DENABLE_BLAS=ON',
        ])

        if self.compiler.name == 'xl' or self.compiler.name == 'xl_r':
            # use F77 compiler if IBM XL
            options.extend([
                '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77,
                '-DCMAKE_Fortran_FLAGS=-qzerosize'
            ])

        if "+i8" in self.spec:
            options.extend(['-DENABLE_I8=ON'])

        return options
