# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spla(CMakePackage):
    """Specialized Parallel Linear Algebra, providing distributed GEMM
    functionality for specific matrix distributions with optional GPU
    acceleration."""

    homepage = "https://github.com/eth-cscs/spla"
    url      = "https://github.com/eth-cscs/spla/archive/v1.0.0.tar.gz"
    git = 'https://github.com/eth-cscs/spla.git'

    version('1.0.0', sha256='a0eb269b84d7525b223dc650de12170bba30fbb3ae4f93eb2b5cbdce335e4da1')
    version('master', branch='master')

    variant('openmp', default=True, description="Build with OpenMP support")
    variant('static', default=False, description="Build as static library")
    variant('cuda', default=False, description="CUDA")

    depends_on('mpi')
    depends_on('blas')
    depends_on('cuda', when='+cuda')
    depends_on('cmake@3.10:', type='build')

    def cmake_args(self):
        args = []

        if '+openmp' in self.spec:
            args += ["-DSPLA_OMP=ON"]
        else:
            args += ["-DSPLA_OMP=OFF"]

        if '+cuda' in self.spec:
            args += ["-DSPLA_GPU_BACKEND=CUDA"]
        else:
            args += ["-DSPLA_GPU_BACKEND=OFF"]

        if '+static' in self.spec:
            args += ["-DSPLA_STATIC=ON"]
        else:
            args += ["-DSPLA_STATIC=OFF"]
        return args
