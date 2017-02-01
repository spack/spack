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


class Elemental(CMakePackage):
    """Elemental: Distributed-memory dense and sparse-direct linear algebra and optimization library."""

    homepage = "http://libelemental.org"
    url      = "https://github.com/elemental/Elemental/archive/v0.87.6.tar.gz"

    version('0.87.6', '9fd29783d45b0a0e27c0df85f548abe9')

    variant('shared', default=True, 
            description='Enables the build of shared libraries')
    variant('hybrid', default=True, 
            description='Elemental: make use of OpenMP within MPI packing/unpacking')
    variant('c_interface', default=False, 
            description='Elemental: build C interface')
    variant('python_package', default=False, 
            description='Elemental: install Python interface')
    variant('disable_parmetis', default=True, 
            description='Elemental: disable ParMETIS')
    variant('disable_quad', default=True, 
            description='Elemental: disable quad precision')
    variant('int64', default=False, 
            description='Elemental: use 64bit integers')
    variant('int64_blas', default=False, 
            description='Elemental: use 64bit integers for BLAS')

    depends_on('cmake', type='build')
    depends_on('openblas +openmp')
    depends_on('metis +int64', when='+int64')
    depends_on('metis', when='~int64')
    depends_on('mpi')
    depends_on('netlib-scalapack')
    def cmake_args(self):
        args = ['-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
                '-DEL_PREFER_OPENBLAS:BOOL=TRUE',
                '-DEL_DISABLE_SCALAPACK:BOOL=OFF',
                '-DMATH_PATHS:STRING=-L{0}/lib -L{1}/lib'.format(
                    self.spec['openblas'].prefix, self.spec['netlib-scalapack'].prefix),
                '-DMATH_LIBS:STRING=-lopenblas -lscalapack',
                '-DGFORTRAN_LIB=libgfortran.so',
                '-DBUILD_SHARED_LIBS:BOOL={0}'.format((
                    'ON' if '+shared' in self.spec else 'OFF')),
                '-DEL_HYBRID:BOOL={0}'.format((
                    'ON' if '+hybrid' in self.spec else 'OFF')),
                '-DEL_C_INTERFACE:BOOL={0}'.format((
                    'ON' if '+c_interface' in self.spec else 'OFF')),
                '-DINSTALL_PYTHON_PACKAGE:BOOL={0}'.format((
                    'ON' if '+python_package' in self.spec else 'OFF')),
                '-DEL_DISABLE_PARMETIS:BOOL={0}'.format((
                    'ON' if '+disable_parmetis' in self.spec else 'OFF')),
                '-DEL_DISABLE_QUAD:BOOL={0}'.format((
                    'ON' if '+disable_quad' in self.spec else 'OFF')),
                '-DEL_USE_64BIT_INTS:BOOL={0}'.format((
                    'ON' if '+int64' in self.spec else 'OFF')),
                '-DEL_USE_64BIT_BLAS_INTS:BOOL={0}'.format((
                    'ON' if '+int64_blas' in self.spec else 'OFF'))]
        return args
