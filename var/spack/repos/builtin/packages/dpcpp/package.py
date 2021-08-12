# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack import *


class Dpcpp(CMakePackage):
    """Data Parallel C++ compiler: Intel's implementation of SYCL programming model"""

    homepage = 'https://intel.github.io/llvm-docs/'
    git = 'https://github.com/intel/llvm.git'

    version('develop', branch='sycl')
    version('stable', commit='7981e6027a8cb43028be55d19f12cb1e30a28f5a')

    maintainers = ['ravil-mobile']
    variant('cuda', default=False, description='switch from OpenCL to CUDA')
    variant('rocm', default=False, description='switch from OpenCL to ROCm')
    variant('rocm-platform', default='AMD', values=('AMD', 'NVIDIA'), multi=False, description='choose ROCm backend')
    variant('arm', default=False, description='build ARM support rather than x86')
    variant('disable-esimd-cpu', default=False, description='build without ESIMD_CPU support')
    variant('no-assertions', default=False, description='build without assertions')
    variant('docs', default=False, description='build Doxygen documentation')
    variant('no-werror', default=False, description='Do not treat warnings as errors')
    variant('shared-libs', default=False, description='Build shared libraries')
    variant('use-lld', default=False, description='Use LLD linker for build')

    depends_on('cmake@3.16.2:', type='build')
    depends_on('ninja@1.10.0:', type='build')

    depends_on('cuda@10.2.0:10.2.999', when='+cuda')

    # NOTE: AMD HIP needs to be tested; it will be done in the next update
    # depends_on('cuda@10.2.89', when='rocm-platform=NVIDIA', type='build')
    # depends_on('hip@4.0.0:', when='+rocm', type='build')

    build_targets = ['deploy-sycl-toolchain']
    install_targets = ['deploy-sycl-toolchain']

    root_cmakelists_dir = 'llvm'

    patch('cuda-backend.patch', when='+cuda')

    def cmake_args(self):
        llvm_external_projects = 'sycl;llvm-spirv;opencl;libdevice;xpti;xptifw'

        sycl_dir = os.path.join(self.stage.source_path, 'sycl')
        spirv_dir = os.path.join(self.stage.source_path, 'llvm-spirv')
        xpti_dir = os.path.join(self.stage.source_path, 'xpti')
        xptifw_dir = os.path.join(self.stage.source_path, 'xptifw')
        libdevice_dir = os.path.join(self.stage.source_path, 'libdevice')
        llvm_targets_to_build = 'X86'
        llvm_enable_projects = 'clang;' + llvm_external_projects
        libclc_targets_to_build = ''
        sycl_build_pi_rocm_platform = self.spec.variants['rocm-platform'].value

        # replace not append, so ARM ^ X86
        if '+arm' in self.spec:
            llvm_targets_to_build = 'ARM;AArch64'

        is_cuda = '+cuda' in self.spec
        is_rocm = '+rocm' in self.spec

        if is_cuda or is_rocm:
            llvm_enable_projects += ';libclc'

        if is_cuda:
            llvm_targets_to_build += ';NVPTX'
            libclc_targets_to_build = 'nvptx64--;nvptx64--nvidiacl'

        if is_rocm:
            if sycl_build_pi_rocm_platform == 'AMD':
                llvm_targets_to_build += ';AMDGPU'
                libclc_targets_to_build += ';amdgcn--;amdgcn--amdhsa'
            elif sycl_build_pi_rocm_platform and not is_cuda:
                llvm_targets_to_build += ';NVPTX'
                libclc_targets_to_build += ';nvptx64--;nvptx64--nvidiacl'

        args = [
            self.define_from_variant('LLVM_ENABLE_ASSERTIONS', 'no-assertions'),
            self.define('LLVM_TARGETS_TO_BUILD', llvm_targets_to_build),
            self.define('LLVM_EXTERNAL_PROJECTS', llvm_external_projects),
            self.define('LLVM_EXTERNAL_SYCL_SOURCE_DIR', sycl_dir),
            self.define('LLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR', spirv_dir),
            self.define('LLVM_EXTERNAL_XPTI_SOURCE_DIR', xpti_dir),
            self.define('XPTI_SOURCE_DIR', xpti_dir),
            self.define('LLVM_EXTERNAL_XPTIFW_SOURCE_DIR', xptifw_dir),
            self.define('LLVM_EXTERNAL_LIBDEVICE_SOURCE_DIR', libdevice_dir),
            self.define('LLVM_ENABLE_PROJECTS', llvm_enable_projects),
            self.define('LIBCLC_TARGETS_TO_BUILD', libclc_targets_to_build),
            self.define('SYCL_BUILD_PI_CUDA', 'ON' if is_cuda else 'OFF'),
            self.define('SYCL_BUILD_PI_ROCM', 'ON' if is_rocm else 'OFF'),
            self.define('SYCL_BUILD_PI_ROCM_PLATFORM', sycl_build_pi_rocm_platform),
            self.define('LLVM_BUILD_TOOLS', True),
            self.define_from_variant('SYCL_ENABLE_WERROR', 'no-werror'),
            self.define('SYCL_INCLUDE_TESTS', True),
            self.define_from_variant('LLVM_ENABLE_DOXYGEN', 'docs'),
            self.define_from_variant('LLVM_ENABLE_SPHINX', 'docs'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared-libs'),
            self.define('SYCL_ENABLE_XPTI_TRACING', 'ON'),
            self.define_from_variant('LLVM_ENABLE_LLD', 'use-lld'),
            self.define_from_variant('SYCL_BUILD_PI_ESIMD_CPU', 'disable-esimd-cpu'),
        ]

        return args

    def setup_run_environment(self, env):
        bin_path = self.spec.prefix.bin
        for env_var_name, compiler in zip(['CC', 'CXX'], ['clang', 'clang++']):
            env.set(env_var_name, os.path.join(bin_path, compiler))

        include_env_vars = ['C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'INCLUDE']
        for var in include_env_vars:
            env.prepend_path(var, self.prefix.include)

        sycl_build_pi_rocm_platform = self.spec.variants['rocm-platform'].value
        if '+cuda' in self.spec or sycl_build_pi_rocm_platform == 'cuda':
            env.prepend_path('PATH', self.spec['cuda'].prefix.bin)
