# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import re


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT/"
    url      = "https://github.com/ROCmSoftwarePlatform/rocfft/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='629f02cfecb7de5ad2517b6a8aac6ed4de60d3a9c620413c4d9db46081ac2c88')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('boost')
    depends_on('fftw-api@3', type='build', when='@3.5:')
    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@3.5:')
    depends_on('hip@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('rocminfo@3.5:', type='build', when='@3.5:')

    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')
        build_env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        build_env.set('DEVICE_LIB_PATH', self.
                      spec['rocm-device-libs'].prefix.lib)

    def setup_run_environment(self, env):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hip-clang')
        env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)

    def cmake_args(self):
        # Finding the version of clang
        hipcc = Executable(join_path(self.spec['hip'].prefix.bin, 'hipcc'))
        version = hipcc('--version', output=str)
        version_group = re.search(r"clang version (\S+)", version)
        version_number = version_group.group(1)

        args = [
            '-DHIP_COMPILER=clang',
            '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(
                self.spec['hip'].prefix),
            '-DUSE_HIP_CLANG=ON',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE',
            '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(
                self.spec['llvm-amdgpu'].prefix, version_number)
        ]
        return args
