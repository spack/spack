# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Raja(CMakePackage, CudaPackage):
    """RAJA Parallel Framework."""

    homepage = "http://software.llnl.gov/RAJA/"
    git      = "https://github.com/LLNL/RAJA.git"

    version('develop', branch='develop', submodules='True')
    version('main',  branch='main',  submodules='True')
    version('0.12.1', tag='v0.12.1', submodules="True")
    version('0.12.0', tag='v0.12.0', submodules="True")
    version('0.11.0', tag='v0.11.0', submodules="True")
    version('0.10.1', tag='v0.10.1', submodules="True")
    version('0.10.0', tag='v0.10.0', submodules="True")
    version('0.9.0', tag='v0.9.0', submodules="True")
    version('0.8.0', tag='v0.8.0', submodules="True")
    version('0.7.0', tag='v0.7.0', submodules="True")
    version('0.6.0', tag='v0.6.0', submodules="True")
    version('0.5.3', tag='v0.5.3', submodules="True")
    version('0.5.2', tag='v0.5.2', submodules="True")
    version('0.5.1', tag='v0.5.1', submodules="True")
    version('0.5.0', tag='v0.5.0', submodules="True")
    version('0.4.1', tag='v0.4.1', submodules="True")
    version('0.4.0', tag='v0.4.0', submodules="True")

    variant('openmp', default=True, description='Build OpenMP backend')
    variant('shared', default=True, description='Build Shared Libs')
    variant('examples', default=True, description='Build examples.')
    variant('exercises', default=True, description='Build exercises.')
    variant('hip', default=False, description='Enable HIP support')

    # possible amd gpu targets for hip builds
    # TODO: we should add a hip build system description equivalent to
    # lib/spack/spack/build_systems/cuda.py, where possible hip amd gpu
    # architectures are defined in a similar way as for cuda gpu
    # architectures. In the meantime, require users to define
    # amd gpu type for hip builds with a variant here.
    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012', 'none'
    )
    variant('amdgpu_target', default='none', values=amdgpu_targets)

    depends_on('llvm-amdgpu', when='+hip')
    depends_on('hip', when='+hip')

    # need amd gpu type for hip builds
    conflicts('amdgpu_target=none', when='+hip')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', when='+cuda', type='build')

    def cmake_args(self):
        spec = self.spec

        options = []
        options.append('-DENABLE_OPENMP={0}'.format(
            'ON' if '+openmp' in spec else 'OFF'))

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
        else:
            options.append('-DENABLE_CUDA=OFF')

        if '+hip' in spec:
            arch = self.spec.variants['amdgpu_target'].value
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix),
                '-DHIP_HCC_FLAGS=--amdgpu-target={0}'.format(arch)])
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DBUILD_SHARED_LIBS={0}'.format(
            'ON' if '+shared' in spec else 'OFF'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))

        options.append('-DENABLE_EXERCISES={0}'.format(
            'ON' if '+exercises' in spec else 'OFF'))

        # Work around spack adding -march=ppc64le to SPACK_TARGET_ARGS which
        # is used by the spack compiler wrapper.  This can go away when BLT
        # removes -Werror from GTest flags
        if self.spec.satisfies('%clang target=ppc64le:') or not self.run_tests:
            options.append('-DENABLE_TESTS=ON')
        else:
            options.append('-DENABLE_TESTS=ON')

        return options
