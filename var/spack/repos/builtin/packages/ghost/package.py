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


class Ghost(CMakePackage, CudaPackage):
    """GHOST: a General, Hybrid and Optimized Sparse Toolkit.
       This library provides highly optimized building blocks for implementing
       sparse iterative eigenvalue and linear solvers multi- and manycore
       clusters and on heterogenous CPU/GPU machines. For an iterative solver
       library using these kernels, see the phist package.
    """

    homepage = "https://www.bitbucket.org/essex/ghost/"
    git      = "https://bitbucket.org/essex/ghost/ghost.git"

    version('develop', branch='devel')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True,
            description='enable/disable MPI')
    variant('scotch', default=False,
            description='enable/disable matrix reordering with PT-SCOTCH')
    variant('zoltan', default=False,
            description='enable/disable matrix reordering with Zoltan')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)
    depends_on('cmake@3.5:')
    depends_on('hwloc')
    depends_on('blas')
    depends_on('mpi', when='+mpi')
    depends_on('scotch', when='+scotch')
    depends_on('zoltan', when='+zoltan')

    def cmake_args(self):
        spec = self.spec
        # note: we require the cblas_include_dir property from the blas
        # provider, this is implemented at least for intel-mkl and
        # netlib-lapack
        args = ['-DGHOST_ENABLE_MPI:BOOL=%s'
                % ('ON' if '+mpi' in spec else 'OFF'),
                '-DGHOST_USE_CUDA:BOOL=%s'
                % ('ON' if '+cuda' in spec else 'OFF'),
                '-DGHOST_USE_SCOTCH:BOOL=%s'
                % ('ON' if '+scotch' in spec else 'OFF'),
                '-DGHOST_USE_ZOLTAN:BOOL=%s'
                % ('ON' if '+zoltan' in spec else 'OFF'),
                '-DBUILD_SHARED_LIBS:BOOL=%s'
                % ('ON' if '+shared' in spec else 'OFF'),
                '-DCBLAS_INCLUDE_DIR:STRING=%s'
                % format(spec['blas'].headers.directories[0]),
                '-DBLAS_LIBRARIES=%s'
                % spec['blas:c'].libs.joined(';')
                ]
        return args

    def check(self):
        make('test')
