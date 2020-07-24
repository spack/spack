# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re
from spack import *


class Rocthrust(CMakePackage):
    """Thrust is a parallel algorithm library. This library has been ported to
       HIP/ROCm platform, which uses the rocPRIM library. The HIP ported
       library works on HIP/ROCm platforms"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocThrust"
    url      = "https://github.com/ROCmSoftwarePlatform/rocThrust/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='0d1bac1129d17bb1259fd06f5c9cb4c1620d1790b5c295b866fb3442d18923cb')

    variant('build_type', default='Release', values=("Release", "Debug"),
            description='CMake build type')

    depends_on('cmake@3.5.2')
    depends_on('hip@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5:', type='build', when='@3.5:')
    depends_on('rocprim@3.5:', type='build', when='@3.5:')

    def cmake_args(self):
        spec = self.spec

        # Finding the version of clang
        hipcc = Executable(join_path(self.spec['hip'].prefix.bin, 'hipcc'))
        version = hipcc('--version', output=str)
        version_group = re.search(r"clang version (\S+)", version)
        version_number = version_group.group(1)

        args = [
            '-DCMAKE_CXX_COMPILER={}/hipcc'.format(spec['hip'].prefix.bin),
            '-DUSE_HIP_CLANG=ON',
            '-DCMAKE_MODULE_PATH={}/cmake'.format(spec['hip'].prefix),
            '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(
                self.spec['llvm-amdgpu'].prefix, version_number)
        ]

        return args
