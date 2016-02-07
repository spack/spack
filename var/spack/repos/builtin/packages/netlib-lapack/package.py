##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class NetlibLapack(Package):
    """
    LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least
    squared solutions to linear sets of equations, eigenvector
    analysis, singular value decomposition, etc. It is a very
    comprehensive and reputable package that has found extensive
    use in the scientific community.
    """
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('debug', default=False, description='Builds the library in debug mode')
    variant('shared', default=True, description='Builds the shared library version')

    # virtual dependency
    provides('lapack')

    # blas is a virtual dependency.
    depends_on('blas', forward=('debug', 'shared'))

    depends_on('cmake')

    # Doesn't always build correctly in parallel
    parallel = False

    def install(self, spec, prefix):
        cmake_args = []
        cmake_args.extend(std_cmake_args)  # Put them first, so that they can be overridden

        cmake_args.append('-DUSE_OPTIMIZED_BLAS:BOOL=ON')
        cmake_args.append('-DBLAS_LIBRARIES:PATH={blas_libraries}'.format(
                blas_libraries=join_path(spec['blas'].prefix.lib, 'libblas.a'))
        )
        if '+shared' in spec:
            cmake_args.extend([
                '-DBUILD_SHARED_LIBS:BOOL=ON',
                '-DBUILD_STATIC_LIBS:BOOL=OFF'
            ])
        else:
            cmake_args.extend([
                '-DBUILD_SHARED_LIBS:BOOL=OFF',
                '-DBUILD_STATIC_LIBS:BOOL=ON'
            ])

        if '+debug' in spec:
            cmake_args.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            cmake_args.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make("install")
