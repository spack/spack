# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "http://arrayfire.org/docs/index.htm"
    git      = "https://github.com/arrayfire/arrayfire.git"

    version('master', submodules=True)
    version('3.7.0', submodules=True, tag='v3.7.0')

    variant('cuda',   default=False, description='Enable Cuda backend')
    variant('opencl', default=False, description='Enable OpenCL backend')

    depends_on('boost')
    depends_on('fftw')
    depends_on('openblas')
    depends_on('cuda', when='+cuda')
    depends_on('opencl', when='+opencl')

    def cmake_args(self):
        args = []
        args.extend([
            '-DAF_BUILD_CUDA={0}'.format(
                'ON' if '+cuda' in self.spec else 'OFF'),
            '-DAF_BUILD_OPENCL={0}'.format(
                'ON' if '+opencl' in self.spec else 'OFF'),
        ])
        return args
