# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    version('2021.09', commit='bd68232bb96386bf7649345c0557ba520e73c02d')
    version('2021.12', commit='27f59d8906fcc8aece7ff6aa570ccdee52168c2d')

    maintainers = ['ravil-mobile']
    variant('cuda', default=False, description='switch from OpenCL to CUDA')
    variant('rocm', default=False, description='switch from OpenCL to ROCm')
    variant('rocm-platform', default='AMD', values=('AMD', 'NVIDIA'), multi=False, description='choose ROCm backend')
    variant('openmp', default=False, description='build with OpenMP without target offloading')
    variant('esimd-cpu', default=False, description='build with ESIMD_CPU support')
    variant('assertions', default=False, description='build with assertions')
    variant('docs', default=False, description='build Doxygen documentation')
    variant('werror', default=False, description='treat warnings as errors')
    variant('shared', default=False, description='build shared libraries')
    variant('remangle_libclc', default=True, description='remangle libclc gen. variants')
    variant('lld', default=False, description='use LLD linker for build')

    depends_on('cmake@3.16.2:', type='build')
    depends_on('ninja@1.10.0:', type='build')

    depends_on('cuda@10.2.0:11.4.999', when='+cuda')

    # NOTE: AMD HIP needs to be tested; it will be done in the next update
    # depends_on('cuda@10.2.0:10.2.999', when='rocm-platform=NVIDIA', type='build')
    # depends_on('hip@4.0.0:', when='+rocm', type='build')

    root_cmakelists_dir = 'llvm'

    def cmake_args(self):
        llvm_external_projects = 'sycl;llvm-spirv;opencl;libdevice;xpti;xptifw'

        if '+openmp' in self.spec:
            llvm_external_projects += ';openmp'

        sycl_dir = os.path.join(self.stage.source_path, 'sycl')
        spirv_dir = os.path.join(self.stage.source_path, 'llvm-spirv')
        xpti_dir = os.path.join(self.stage.source_path, 'xpti')
        xptifw_dir = os.path.join(self.stage.source_path, 'xptifw')
        libdevice_dir = os.path.join(self.stage.source_path, 'libdevice')
        llvm_enable_projects = 'clang;' + llvm_external_projects
        libclc_targets_to_build = ''
        sycl_build_pi_rocm_platform = self.spec.variants['rocm-platform'].value

        if self.spec.satisfies('target=x86_64:'):
            llvm_targets_to_build = 'X86'
        elif self.spec.satisfies('target=aarch64:'):
            llvm_targets_to_build = 'ARM;AArch64'
        else:
            raise InstallError('target is not supported. '
                               'This package only works on x86_64 or aarch64')

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
            self.define_from_variant('LLVM_ENABLE_ASSERTIONS', 'assertions'),
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
            self.define_from_variant('SYCL_BUILD_PI_CUDA', 'cuda'),
            self.define_from_variant('SYCL_BUILD_PI_ROCM', 'rocm'),
            self.define('SYCL_BUILD_PI_ROCM_PLATFORM', sycl_build_pi_rocm_platform),
            self.define('LLVM_BUILD_TOOLS', True),
            self.define_from_variant('SYCL_ENABLE_WERROR', 'werror'),
            self.define('SYCL_INCLUDE_TESTS', True),
            self.define_from_variant('LIBCLC_GENERATE_REMANGLED_VARIANTS',
                                     'remangle_libclc'),
            self.define_from_variant('LLVM_ENABLE_DOXYGEN', 'docs'),
            self.define_from_variant('LLVM_ENABLE_SPHINX', 'docs'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('SYCL_ENABLE_XPTI_TRACING', 'ON'),
            self.define_from_variant('LLVM_ENABLE_LLD', 'lld'),
            self.define_from_variant('SYCL_BUILD_PI_ESIMD_CPU', 'esimd-cpu'),
        ]

        if is_cuda or (is_rocm and sycl_build_pi_rocm_platform == 'NVIDIA'):
            args.append(
                self.define('CUDA_TOOLKIT_ROOT_DIR', self.spec['cuda'].prefix)
            )

        if '+openmp' in self.spec:
            omp_dir = os.path.join(self.stage.source_path, 'openmp')
            args.extend([
                self.define('LLVM_EXTERNAL_OPENMP_SOURCE_DIR', omp_dir),
                self.define('OPENMP_ENABLE_LIBOMPTARGET', False),
            ])

        if self.compiler.name == 'gcc':
            gcc_prefix = ancestor(self.compiler.cc, 2)
            args.append(self.define('GCC_INSTALL_PREFIX', gcc_prefix))

        return args

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            env.set('CUDA_LIB_PATH', '{0}/lib64/stubs'.format(self.spec['cuda'].prefix))

    @run_after("install")
    def post_install(self):
        clang_cpp_path = os.path.join(self.spec.prefix.bin, 'clang++')
        dpcpp_path = os.path.join(self.spec.prefix.bin, 'dpcpp')

        real_clang_cpp_path = os.path.realpath(clang_cpp_path)
        os.symlink(real_clang_cpp_path, dpcpp_path)

    def setup_run_environment(self, env):
        bin_path = self.spec.prefix.bin
        for env_var_name, compiler in zip(['CC', 'CXX'], ['clang', 'clang++']):
            env.set(env_var_name, os.path.join(bin_path, compiler))

        include_env_vars = ['C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'INCLUDE']
        for var in include_env_vars:
            env.prepend_path(var, self.prefix.include)
            env.prepend_path(var, self.prefix.include.sycl)

        sycl_build_pi_rocm_platform = self.spec.variants['rocm-platform'].value
        if '+cuda' in self.spec or sycl_build_pi_rocm_platform == 'NVIDIA':
            env.prepend_path('PATH', self.spec['cuda'].prefix.bin)
            env.set('CUDA_TOOLKIT_ROOT_DIR', self.spec['cuda'].prefix)
