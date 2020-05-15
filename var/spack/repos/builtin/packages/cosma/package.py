# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosma(CMakePackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    maintainers = ['haampie', 'kabicm', 'teonnik']
    homepage = 'https://github.com/eth-cscs/COSMA'
    url = 'https://github.com/eth-cscs/COSMA/releases/download/v2.2.0/cosma.tar.gz'
    git = 'https://github.com/eth-cscs/COSMA.git'

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version('master', branch='master', submodules=True)
    version('2.2.0', '8f3c6b9235c83092777a958bda37bfc2fa2b0da4')
    version('2.0.7', '70d0d9ab45f2af3d06c5c0e856e28b2adb246ff9')
    version('2.0.2', 'fcedd19be56ca75d122782f29872923d9bead847')

    variant('gpu', default=False,
            description='Build with the GPU back end.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK API.')

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi@3:')
    depends_on('blas', when='~gpu')
    depends_on('scalapack', when='+scalapack')
    # COSMA is written entirely in C/C++, it may use cublas but a CUDA capable
    # compiler is not needed. There is no need for CudaPackage in this recipe.
    depends_on('cuda', when='+gpu')

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
        elif '^cray-libsci' in spec:
            args += ['-DCOSMA_BLAS=CRAY_LIBSCI']
        elif '^netlib-lapack' in spec:
            args += ['-DCOSMA_BLAS=CUSTOM']
        elif '^openblas' in spec:
            args += ['-DCOSMA_BLAS=OPENBLAS']
        elif '+gpu' in spec:
            args += ['-DCOSMA_BLAS=CUDA']
        else:  # TODO '^rocm' in spec:
            args += ['-DCOSMA_BLAS=ROCM']

        if '+scalapack' and '^mkl' in spec:
            args += ['-DCOSMA_SCALAPACK=MKL']
        elif '+scalapack' and '^cray-libsci' in spec:
            args += ['-DCOSMA_SCALAPACK=CRAY_LIBSCI']
        elif '+scalapack' and '^netlib-scalapack' in spec:
            args += ['-DCOSMA_SCALAPACK=CUSTOM']

        return args
