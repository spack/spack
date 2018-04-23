##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@us.ibm.com, All rights reserved.
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


class Magma(CMakePackage):
    """The MAGMA project aims to develop a dense linear algebra library similar to
       LAPACK but for heterogeneous/hybrid architectures, starting with current
       "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"

    version('2.3.0', '9aaf85a338d3a17303e0c69f86f0ec52')
    version('2.2.0', '6c1ebf4cdf63eb302ff6258ff8c49217')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')
    variant('shared', default=True,
            description='Enable shared library')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda')

    conflicts('%gcc@6:', when='^cuda@:8')
    conflicts('%gcc@7:', when='^cuda@:9')

    patch('ibm-xl.patch', when='@2.2:%xl')
    patch('ibm-xl.patch', when='@2.2:%xl_r')
    patch('magma-2.3.0-gcc-4.8.patch', when='@2.3.0%gcc@:4.8')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix,
            '-DBLAS_LIBRARIES=%s' % spec['blas'].libs.joined(';'),
            # As of MAGMA v2.3.0, CMakeLists.txt does not use the variable
            # BLAS_LIBRARIES, but only LAPACK_LIBRARIES, so we need to
            # explicitly add blas to LAPACK_LIBRARIES.
            '-DLAPACK_LIBRARIES=%s' %
            (spec['lapack'].libs + spec['blas'].libs).joined(';')
        ])

        options += ['-DBUILD_SHARED_LIBS=%s' %
                    ('ON' if ('+shared' in spec) else 'OFF')]

        if '+fortran' in spec:
            options.extend([
                '-DUSE_FORTRAN=yes'
            ])
            if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
                options.extend([
                    '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77
                ])

        if spec.satisfies('^cuda@9.0:'):
            if '@:2.2.0' in spec:
                options.extend(['-DGPU_TARGET=sm30'])
            else:
                options.extend(['-DGPU_TARGET=sm_30'])

        return options

    @run_after('install')
    def post_install(self):
        install('magmablas/atomics.cuh', self.prefix.include)
        install('control/magma_threadsetting.h', self.prefix.include)
        install('control/pthread_barrier.h', self.prefix.include)
        install('control/magma_internal.h', self.prefix.include)
