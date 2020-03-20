# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install dlib
#
# You can edit this file again by typing:
#
#     spack edit dlib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Dlib(CMakePackage):
    """Dlib is a modern C++ toolkit containing machine learning
    algorithms and tools for creating complex software in C++
    to solve real world problems.
    """

    homepage = "http://dlib.net"
    url      = "https://github.com/davisking/dlib/archive/v19.19.tar.gz"

    version('19.19', sha256='7af455bb422d3ae5ef369c51ee64e98fa68c39435b0fa23be2e5d593a3d45b87')

    variant('cuda', default=False, description='Build with CUDA')
    variant('blas', default=True, description='Build with BLAS')
    variant('lapack', default=True, description='Build with LAPACK')
    variant('mkl', default=False, description='Build with the MKL library')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('tbb', 'none'),
        multi=False
    )
    variant('avx', default=False, description='Use AVX instructions')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda', when='+cuda')
    depends_on('mkl threads=none', when='+mkl threads=none')
    depends_on('mkl threads=mkl', when='+mkl threads=mkl')

    def cmake_args(self):
        args = [
            '-DDLIB_USE_BLAS=ON',
            '-DDLIB_USE_LAPACK=ON'
        ]

        if '+cuda' in self.spec:
            args.append('-DDLIB_USE_CUDA=ON')
        else:
            args.append('-DDLIB_USE_CUDA=OFF')

        if '+mkl threads=none' in self.spec:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=ON')
            args.append('-DDLIB_USE_MKL_TBB=OFF')
        elif '+mkl threads=tbb' in self.spec:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=OFF')
            args.append('-DDLIB_USE_MKL_TBB=ON')
        else:
            args.append('-DDLIB_USE_MKL_SEQUENTIAL=OFF')
            args.append('-DDLIB_USE_MKL_TBB=OFF')

        if '+avx' in self.spec:
            args.append('-DUSE_AVX_INSTRUCTIONS=ON')
        else:
            args.append('-DUSE_AVX_INSTRUCTIONS=OFF')
        
        return args
