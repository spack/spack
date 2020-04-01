# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/pghysels/STRUMPACK/archive/v3.3.0.tar.gz"
    git      = "https://github.com/pghysels/STRUMPACK.git"

    maintainers = ['pghysels']

    version('master', branch='master')
    version('3.3.0', sha256='499fd3b58656b4b6495496920e5372895861ebf15328be8a7a9354e06c734bc7')
    version('3.2.0', sha256='34d93e1b2a3b8908ef89804b7e08c5a884cbbc0b2c9f139061627c0d2de282c1')
    version('3.1.1', sha256='c1c3446ee023f7b24baa97b24907735e89ce4ae9f5ef516645dfe390165d1778')
    version('3.1.0', sha256='b4f91b7d433955518b04538be1c726afc5de4bffb163e982ef8844d391b26fa7')
    version('3.0.3', sha256='2bd2a40d9585b769ae4ba461de02c6e36433bf2b21827f824a50f2fdf73389f7')
    version('3.0.2', sha256='828e5ec59019b2c74e008745b04ceebbb7ef1313fb4e3ac01fa8ff350799df38')
    version('3.0.1', sha256='b4a4d870c589937e22e77a6c4b52a96fd808f0b564e363f826ae5ffc94b9d000')
    version('3.0.0', sha256='7acd9b4653b8b11380de733c80b164348ca00f9226904f5dc166a8e3db88cd20')
    version('2.2.0', sha256='8fe73875cbbb29ed1faf714e3bf13ad538eb062e39d7d5e73cb9c4aafb571e24')

    variant('shared', default=False, description='Build shared libraries')
    variant('mpi', default=True, description='Use MPI')
    variant('openmp', default=True,
            description='Enable thread parallellism via tasking with OpenMP')
    variant('parmetis', default=False,
            description='Enable use of ParMetis')
    variant('scotch', default=False,
            description='Enable use of Scotch')
    variant('butterflypack', default=True,
            description='Enable use of ButterflyPACK')
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

    depends_on('cmake@3.2:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scotch~metis', when='+scotch')
    depends_on('scotch~metis+mpi', when='+scotch+mpi')
    depends_on('butterflypack@1.1.0:', when='+butterflypack+mpi')

    conflicts('+parmetis', when='~mpi')
    conflicts('+butterflypack', when='~mpi')
    conflicts('+butterflypack', when='strumpack@:3.2.0')

    patch('intel-19-compile.patch', when='@3.1.1')

    def cmake_args(self):
        spec = self.spec

        def on_off(varstr):
            return 'ON' if varstr in spec else 'OFF'

        if '+mpi' in spec:
            args = ['-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                    '-DSTRUMPACK_USE_MPI=ON']
        else:
            args = ['-DSTRUMPACK_USE_MPI=OFF']

        args.extend([
            '-DSTRUMPACK_USE_OPENMP=%s' % on_off('+openmp'),
            '-DSTRUMPACK_C_INTERFACE=%s' % on_off('+c_interface'),
            '-DSTRUMPACK_COUNT_FLOPS=%s' % on_off('+count_flops'),
            '-DSTRUMPACK_TASK_TIMERS=%s' % on_off('+task_timers'),
            '-DSTRUMPACK_DEV_TESTING=%s' % on_off('+build_dev_tests'),
            '-DSTRUMPACK_BUILD_TESTS=%s' % on_off('+build_tests')
        ])

        if spec.satisfies('@3.0.4:'):
            args.extend([
                '-DTPL_ENABLE_PARMETIS=%s' % on_off('+parmetis'),
                '-DTPL_ENABLE_SCOTCH=%s' % on_off('+scotch'),
                '-DTPL_ENABLE_BPACK=%s' % on_off('+butterflypack')
            ])
        else:
            args.extend([
                '-DSTRUMPACK_USE_PARMETIS=%s' % on_off('+parmetis'),
                '-DSTRUMPACK_USE_SCOTCH=%s' % on_off('+scotch')
            ])

        args.extend([
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared')
        ])

        return args
