# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosma(CMakePackage, CudaPackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    homepage = "https://github.com/eth-cscs/COSMA"
    maintainers = ['teonnik', 'kabicm']

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version('develop',
            git='https://github.com/eth-cscs/COSMA.git',
            branch='master',
            submodules=True)
    version('2.0.2',
            url='https://github.com/eth-cscs/COSMA/releases/download/v2.0.2/cosma.tar.gz',
            sha256='4f3354828bc718f3eef2f0098c3bdca3499297497a220da32db1acd57920c68d')
    # note: this version fails to build at the moment
    # version('1.0.0',
    #         url='https://github.com/eth-cscs/COSMA/releases/download/1.0/cosma.tar.gz',
    #         sha256='c142104258dcca4c17fa7faffc2990a08d2777235c7980006e93c5dca51061f6')

    variant('blas', default='mkl',
            values=('mkl', 'openblas', 'netlib', 'cuda', 'rocm'),
            description='BLAS backend')
    variant('scalapack', default='none',
            values=('mkl', 'netlib'),
            description='Optional ScaLAPACK support.')

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi@3:')

    depends_on('intel-mkl', when='blas=mkl')
    depends_on('openblas', when='blas=openblas')
    depends_on('netlib-lapack', when='blas=netlib')
    depends_on('netlib-scalapack', when='scalapack=netlib')
    depends_on('cuda', when='blas=cuda')
    # TODO: rocm

    def setup_build_environment(self, env):
        if 'blas=cuda' in self.spec:
            env.set('CUDA_PATH', self.spec['cuda'].prefix)

    def cmake_args(self):
        spec = self.spec
        args = ['-DCOSMA_WITH_TESTS=OFF',
                '-DCOSMA_WITH_APPS=OFF',
                '-DCOSMA_WITH_PROFILING=OFF',
                '-DCOSMA_WITH_BENCHMARKS=OFF']

        if 'blas=mkl' in spec:
            args += ['-DCOSMA_BLAS=MKL']
        elif 'blas=netlib' in spec:
            args += ['-DCOSMA_BLAS=CUSTOM']
        elif 'blas=openblas' in spec:
            args += ['-DCOSMA_BLAS=OPENBLAS']
        elif 'blas=cuda' in spec:
            args += ['-DCOSMA_BLAS=CUDA']
        else:  # 'blas=rocm' in spec:
            args += ['-DCOSMA_BLAS=ROCM']

        if 'scalapack=mkl' in spec:
            args += ['-DCOSMA_SCALAPACK=MKL']
        elif 'scalapack=netlib' in spec:
            args += ['-DCOSMA_SCALAPACK=CUSTOM']

        return args
