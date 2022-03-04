# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Camp(CMakePackage, CudaPackage, ROCmPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git      = "https://github.com/LLNL/camp.git"
    url      = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    maintainers = ['trws']

    version('main', branch='main', submodules='True')
    version('0.5.3', sha256='360ecabc764c85740559d633282fb640e021a2b8b494593c8871f72420366ec1')
    version('0.3.0', sha256='129431a049ca5825443038ad5a37a86ba6d09b2618d5fe65d35f83136575afdb')
    version('0.2.3', sha256='58a0f3bd5eadb588d7dc83f3d050aff8c8db639fc89e8d6553f9ce34fc2421a7')
    version('0.2.2', sha256='194d38b57e50e3494482a7f94940b27f37a2bee8291f2574d64db342b981d819')
    version('0.1.0', sha256='fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc')

    # TODO: figure out gtest dependency and then set this default True.
    variant('tests', default=False, description='Build tests')

    depends_on('cub', when='+cuda')

    depends_on('blt')

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append("-DBLT_SOURCE_DIR={0}".format(spec['blt'].prefix))

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

        if '+rocm' in spec:
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix)
            ])
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                options.append(
                    '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.format(arch_str)
                )
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append(self.define_from_variant('ENABLE_TESTS', 'tests'))

        return options
