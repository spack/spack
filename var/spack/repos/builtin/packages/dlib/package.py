# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dlib(CMakePackage):
    """Dlib is a modern C++ toolkit containing machine learning
    algorithms and tools for creating complex software in C++
    to solve real world problems."""

    homepage = "http://dlib.net"
    url      = "https://github.com/davisking/dlib/archive/v19.19.tar.gz"

    version('19.19', sha256='7af455bb422d3ae5ef369c51ee64e98fa68c39435b0fa23be2e5d593a3d45b87')

    variant('cuda', default=False, description='Build with CUDA')
    variant('blas', default=True, description='Build with BLAS')
    variant('lapack', default=True, description='Build with LAPACK')
    variant('mkl', default=False, description='Build with the MKL library')
    variant('avx', default=False, description='Use AVX instructions')
    variant('shared', default=False, description='Build shared libraries')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda', when='+cuda')
    depends_on('mkl', when='+mkl')

    def cmake_args(self):
        args = []

        if '+blas' in self.spec:
            args.append('-DDLIB_USE_BLAS=ON')
        else:
            args.append('-DDLIB_USE_BLAS=OFF')

        if '+lapack' in self.spec:
            args.append('-DDLIB_USE_LAPACK=ON')
        else:
            args.append('-DDLIB_USE_LAPACK=OFF')

        if '+cuda' in self.spec:
            args.append('-DDLIB_USE_CUDA=ON')
        else:
            args.append('-DDLIB_USE_CUDA=OFF')

        if '^mkl threads=none' in self.spec:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=ON')
            args.append('-DDLIB_USE_MKL_TBB=OFF')
        elif '^mkl threads=tbb' in self.spec:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=OFF')
            args.append('-DDLIB_USE_MKL_TBB=ON')
        else:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=OFF')
            args.append('-DDLIB_USE_MKL_TBB=OFF')

        if '+avx' in self.spec:
            args.append('-DUSE_AVX_INSTRUCTIONS=ON')
        else:
            args.append('-DUSE_AVX_INSTRUCTIONS=OFF')

        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        return args
