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


class NetlibBlas(Package):
    """
    Netlib reference BLAS
    """
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    variant('debug', default=False, description='Builds the library in debug mode')
    variant('shared', default=True, description='Builds the shared library version')

    # virtual dependency
    provides('blas')

    # Doesn't always build correctly in parallel
    parallel = False

    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)
        options.append('-DUSE_OPTIMIZED_BLAS:BOOL=OFF')  # to force it to create the blas target

        if '+shared' in spec:
            options.extend([
                '-DBUILD_SHARED_LIBS:BOOL=ON',
                '-DBUILD_STATIC_LIBS:BOOL=OFF'
            ])
        else:
            options.extend([
                '-DBUILD_SHARED_LIBS:BOOL=OFF',
                '-DBUILD_STATIC_LIBS:BOOL=ON'
            ])

        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        with working_dir('spack-build', create=True):
            cmake('..', *options)

        with working_dir('spack-build/BLAS'):
            make()
            make('test')
            make('install')
