# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Strumpack(CMakePackage):
    """STRUMPACK -- STRUctured Matrix PACKage - provides linear solvers
    for sparse matrices and for dense rank-structured matrices, i.e.,
    matrices that exhibit some kind of low-rank property. It provides a
    distributed memory fully algebraic sparse solver and
    preconditioner. The preconditioner is mostly aimed at large sparse
    linear systems which result from the discretization of a partial
    differential equation, but is not limited to any particular type of
    problem. STRUMPACK also provides preconditioned GMRES and BiCGStab
    iterative solvers."""

    homepage = "http://portal.nersc.gov/project/sparse/strumpack"
    url      = "https://github.com/pghysels/STRUMPACK/archive/v3.0.3.tar.gz"
    git      = "https://github.com/pghysels/STRUMPACK.git"

    version('master', branch='master')
    version('3.0.3', sha256='2bd2a40d9585b769ae4ba461de02c6e36433bf2b21827f824a50f2fdf73389f7')
    version('3.0.2', sha256='828e5ec59019b2c74e008745b04ceebbb7ef1313fb4e3ac01fa8ff350799df38')
    version('3.0.1', sha256='b4a4d870c589937e22e77a6c4b52a96fd808f0b564e363f826ae5ffc94b9d000')
    version('3.0.0', sha256='7acd9b4653b8b11380de733c80b164348ca00f9226904f5dc166a8e3db88cd20')
    version('2.2.0', sha256='8fe73875cbbb29ed1faf714e3bf13ad538eb062e39d7d5e73cb9c4aafb571e24')

    variant('mpi', default=True, description='Use MPI')
    variant('openmp', default=True,
            description='Enable thread parallellism via tasking with OpenMP')
    variant('parmetis', default=False,
            description='Enable use of ParMetis')
    variant('scotch', default=False,
            description='Enable use of Scotch')
    variant('c_interface', default=True,
            description='Enable C interface')
    variant('count_flops', default=False,
            description='Build with flop counters')
    variant('task_timers', default=False,
            description='Build with timers for internal routines')
    variant('build_dev_tests', default=False,
            description='Build developer test routines')
    variant('build_tests', default=False,
            description='Build test routines')

    depends_on('cmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+parmetis+mpi')
    depends_on('scotch~metis', when='+scotch')
    depends_on('scotch~metis+mpi', when='+scotch+mpi')

    def cmake_args(self):
        spec = self.spec

        if '+mpi' in spec:
            args = ['-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                    '-DSTRUMPACK_USE_MPI=ON']
        else:
            args = ['-DSTRUMPACK_USE_MPI=OFF']

        if '+openmp' in spec:
            args.append('-DSTRUMPACK_USE_OPENMP=ON')
        else:
            args.append('-DSTRUMPACK_USE_OPENMP=OFF')

        if spec.satisfies('+parmetis+mpi'):
            args.append('-DSTRUMPACK_USE_PARMETIS=ON')
        else:
            args.append('-DSTRUMPACK_USE_PARMETIS=OFF')

        if '+scotch' in spec:
            args.append('-DSTRUMPACK_USE_SCOTCH=ON')
        else:
            args.append('-DSTRUMPACK_USE_SCOTCH=OFF')

        if '+c_interface' in spec:
            args.append('-DSTRUMPACK_C_INTERFACE=ON')
        else:
            args.append('-DSTRUMPACK_C_INTERFACE=OFF')

        if '+count_flops' in spec:
            args.append('-DSTRUMPACK_COUNT_FLOPS=ON')
        else:
            args.append('-DSTRUMPACK_COUNT_FLOPS=OFF')

        if '+task_timers' in spec:
            args.append('-DSTRUMPACK_TASK_TIMERS=ON')
        else:
            args.append('-DSTRUMPACK_TASK_TIMERS=OFF')

        if '+build_dev_tests' in spec:
            args.append('-DSTRUMPACK_DEV_TESTING=ON')
        else:
            args.append('-DSTRUMPACK_DEV_TESTING=OFF')

        if '+build_tests' in spec:
            args.append('-DSTRUMPACK_BUILD_TESTS=ON')
        else:
            args.append('-DSTRUMPACK_BUILD_TESTS=OFF')
        return args
