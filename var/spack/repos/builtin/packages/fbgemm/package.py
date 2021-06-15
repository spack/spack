# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fbgemm(CMakePackage):
    """FBGEMM (Facebook GEneral Matrix Multiplication) is a low-precision,
    high-performance matrix-matrix multiplications and convolution library
    for server-side inference."""

    homepage = "https://github.com/pytorch/FBGEMM"
    git      = "https://github.com/pytorch/FBGEMM.git"

    maintainers = ['dskhudia']

    version('master', branch='master', submodules=True)

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')
    depends_on('llvm-openmp', when='%apple-clang')

    generator = 'Ninja'
