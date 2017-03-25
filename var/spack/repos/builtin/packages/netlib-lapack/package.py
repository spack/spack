#############################################################################
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


class NetlibLapack(Package):
    """LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least squared
    solutions to linear sets of equations, eigenvector analysis, singular
    value decomposition, etc. It is a very comprehensive and reputable
    package that has found extensive use in the scientific community.

    """
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.6.1', '421b2cb72e15f237e144428f9c460ee0')
    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('debug', default=False, description='Activates the Debug build type')
    variant('shared', default=True, description="Build shared library version")
    variant('external-blas', default=False,
            description='Build lapack with an external blas')

    variant('lapacke', default=True,
            description='Activates the build of the LAPACKE C interface')

    patch('ibm-xl.patch', when='@3:6%xl')
    patch('ibm-xl.patch', when='@3:6%xl_r')

    # virtual dependency
    provides('blas', when='~external-blas')
    provides('lapack')

    depends_on('cmake', type='build')
    depends_on('blas', when='+external-blas')

    def patch(self):
        # Fix cblas CMakeLists.txt -- has wrong case for subdirectory name.
        if self.spec.satisfies('@3.6.0:'):
            filter_file(
                '${CMAKE_CURRENT_SOURCE_DIR}/CMAKE/',
                '${CMAKE_CURRENT_SOURCE_DIR}/cmake/',
                'CBLAS/CMakeLists.txt', string=True)

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libblas', root=self.prefix, shared=shared, recurse=True
        )

    @property
    def lapack_libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'liblapack', root=self.prefix, shared=shared, recurse=True
        )

    def install_one(self, spec, prefix, shared):
        cmake_args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if shared else 'OFF'),
            '-DCMAKE_BUILD_TYPE:STRING=%s' % (
                'Debug' if '+debug' in spec else 'Release'),
            '-DLAPACKE:BOOL=%s' % ('ON' if '+lapacke' in spec else 'OFF')]
        if spec.satisfies('@3.6.0:'):
            cmake_args.extend(['-DCBLAS=ON'])  # always build CBLAS

        if self.compiler.name == 'intel':
            # Intel compiler finds serious syntax issues when trying to
            # build CBLAS and LapackE
            cmake_args.extend(['-DCBLAS=OFF'])
            cmake_args.extend(['-DLAPACKE:BOOL=OFF'])

        if self.compiler.name == 'xl' or self.compiler.name == 'xl_r':
            # use F77 compiler if IBM XL
            cmake_args.extend([
                '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77,
                '-DCMAKE_Fortran_FLAGS=-qzerosize'
            ])

        # deprecated routines are commonly needed by, for example, suitesparse
        # Note that OpenBLAS spack is built with deprecated routines
        cmake_args.extend(['-DBUILD_DEPRECATED:BOOL=ON'])

        if '+external-blas' in spec:
            cmake_args.extend([
                '-DUSE_OPTIMIZED_BLAS:BOOL=ON',
                '-DBLAS_LIBRARIES:PATH=%s' % spec['blas'].libs.joined(';')
            ])

        cmake_args.extend(std_cmake_args)

        build_dir = 'spack-build' + ('-shared' if shared else '-static')
        with working_dir(build_dir, create=True):
            cmake('..', *cmake_args)
            make()
            make("install")

    def install(self, spec, prefix):
        # Always build static libraries.
        self.install_one(spec, prefix, False)

        # Build shared libraries if requested.
        if '+shared' in spec:
            self.install_one(spec, prefix, True)
