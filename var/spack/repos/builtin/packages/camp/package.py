# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Camp(CMakePackage, CudaPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git      = "https://github.com/LLNL/camp.git"

    version('master', branch='master', submodules='True')
    version('0.1.0', url='https://github.com/LLNL/camp/archive/v0.1.0.tar.gz')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', type='build', when="+cuda")

    variant('hip', default=False, description='Enable HIP support')
    depends_on('llvm-amdgpu', when='+hip')
    depends_on('hip', when='+hip')

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))
        else:
            options.append('-DENABLE_CUDA=OFF')

        # Please note that there is currently a bug in how spack detects hip.
        # There is a workaound involving some manual changes to the hip
        # package file and to the packages.yaml file.
        # Please contact a developer for details.
        if '+hip' in spec:
            # Possibly add '-DHIP_CLANG_PATH={0}'
            #  .format(self.spec['llvm-amdgpu'].prefix.bin
            # in the future if there are issues.
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'. format(spec['hip'].prefix)])
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DENABLE_TESTS=ON')

        return options
