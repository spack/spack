# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dbcsr(CMakePackage):
    """Distributed Block Compressed Sparse Row matrix library."""

    homepage = "https://github.com/cp2k/dbcsr"
    git      = "https://github.com/cp2k/dbcsr.git"

    version('develop', branch='develop')

    variant('mpi',    default=True,  description='Compile with MPI')
    variant('openmp', default=False, description='Build with OpenMP support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('py-fypp')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DUSE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DUSE_OPENMP=%s' % (
                'ON' if '+openmp' in spec else 'OFF'),
            # C API need MPI
            '-DWITH_C_API=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(';'),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES=%s' % spec['blas'].libs.joined(';'),
            '-DWITH_EXAMPLES=ON',
            '-DBUILD_SHARED_LIBS=ON'
        ]

        return args
