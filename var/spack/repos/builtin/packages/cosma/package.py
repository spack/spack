# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosma(CMakePackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    maintainers = ['teonnik', 'kabicm']
    homepage = 'https://github.com/eth-cscs/COSMA'
    url = 'https://github.com/eth-cscs/COSMA/releases/download/v2.0.2/cosma.tar.gz'
    git = 'https://github.com/eth-cscs/COSMA.git'

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version('master', branch='master', submodules=True)
    version('2.0.2', sha256='4f3354828bc718f3eef2f0098c3bdca3499297497a220da32db1acd57920c68d')
    # note: this version fails to build at the moment
    # version('1.0.0',
    #         url='https://github.com/eth-cscs/COSMA/releases/download/1.0/cosma.tar.gz',
    #         sha256='c142104258dcca4c17fa7faffc2990a08d2777235c7980006e93c5dca51061f6')

    variant('cuda', default=False,
            description='Build with the CUBLAS back end.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK support.')

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi@3:')
    depends_on('blas', when='~cuda')
    depends_on('scalapack', when='+scalapack')
    # COSMA is written entirely in C++, it may use cublasXt but a CUDA capable
    # compiler is not needed. There is no need for CudaPackage in this recipe.
    depends_on('cuda', when='+cuda')

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            env.set('CUDA_PATH', self.spec['cuda'].prefix)

    def cmake_args(self):
        spec = self.spec
        args = ['-DCOSMA_WITH_TESTS=OFF',
                '-DCOSMA_WITH_APPS=OFF',
                '-DCOSMA_WITH_PROFILING=OFF',
                '-DCOSMA_WITH_BENCHMARKS=OFF']

        if '^mkl' in spec:
            args += ['-DCOSMA_BLAS=MKL']
        elif '^netlib-lapack' in spec:
            args += ['-DCOSMA_BLAS=CUSTOM']
        elif '^openblas' in spec:
            args += ['-DCOSMA_BLAS=OPENBLAS']
        elif '+cuda' in spec:
            args += ['-DCOSMA_BLAS=CUDA']
        else:  # TODO '^rocm' in spec:
            args += ['-DCOSMA_BLAS=ROCM']

        if '+scalapack' and '^mkl' in spec:
            args += ['-DCOSMA_SCALAPACK=MKL']
        elif '+scalapack' and '^netlib-scalapack' in spec:
            args += ['-DCOSMA_SCALAPACK=CUSTOM']

        return args
