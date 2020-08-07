# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
       create portable applications for AMD and NVIDIA GPUs from
       single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    url      = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3')

    depends_on('cmake@3:', type='build')
    depends_on('rocclr@3.5.0',  when='@3.5.0')
    depends_on('hsakmt-roct@3.5.0', type='build', when='@3.5.0')
    depends_on('hsa-rocr-dev@3.5.0', type='link', when='@3.5.0')
    depends_on('comgr@3.5.0', type='build', when='@3.5.0')
    depends_on('llvm-amdgpu@3.5.0', type='build', when='@3.5.0')
    depends_on('rocm-device-libs', type='build')
    depends_on('rocminfo@3.5.0', type='build', when='@3.5.0')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)

        # We have directories hipcc cannot infer
        env.set('HSA_PATH', self.spec['hsa-rocr-dev'].prefix)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)

        # HIP_COMPILER and HIP_PLATFORM are autodetected by hipcc

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, 'hipcc')

    def patch(self):
        filter_file(
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
            'hip-config.cmake.in', string=True)

    def cmake_args(self):
        args = [
            '-DHIP_COMPILER=clang',
            '-DHIP_PLATFORM=rocclr',
            '-DHSA_PATH={0}'.format(self.spec['hsa-rocr-dev'].prefix),
            '-DLIBROCclr_STATIC_DIR={0}/lib'.format(self.spec['rocclr'].prefix)
        ]
        return args
