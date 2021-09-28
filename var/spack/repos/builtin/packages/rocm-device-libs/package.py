# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs"
    git      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs.git"
    url      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-4.3.1.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='amd-stg-open')
    version('4.3.1', sha256='a7291813168e500bfa8aaa5d1dccf5250764ddfe27535def01b51eb5021d4592')
    version('4.3.0', sha256='055a67e63da6491c84cd45865500043553fb33c44d538313dd87040a6f3826f2')
    version('4.2.0', sha256='34a2ac39b9bb7cfa8175cbab05d30e7f3c06aaffce99eed5f79c616d0f910f5f')
    version('4.1.0', sha256='f5f5aa6bfbd83ff80a968fa332f80220256447c4ccb71c36f1fbd2b4a8e9fc1b')
    version('4.0.0', sha256='d0aa495f9b63f6d8cf8ac668f4dc61831d996e9ae3f15280052a37b9d7670d2a')
    version('3.10.0', sha256='bca9291385d6bdc91a8b39a46f0fd816157d38abb1725ff5222e6a0daa0834cc')
    version('3.9.0', sha256='c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7')
    version('3.8.0', sha256='e82cc9a8eb7d92de02cabb856583e28f17a05c8cf9c97aec5275608ef1a38574')
    version('3.7.0', sha256='b3a114180bf184b3b829c356067bc6a98021d52c1c6f9db6bc57272ebafc5f1d')
    version('3.5.0', sha256='dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('zlib', type='link', when='@3.9.0:')
    depends_on('texinfo', type='link', when='@3.9.0:')

    # Make sure llvm is not built with rocm-device-libs (that is, it's already
    # built with rocm-device-libs as an external project).
    depends_on('llvm-amdgpu ~rocm-device-libs')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', 'master']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,              when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        return [
            self.define('LLVM_DIR', spec['llvm-amdgpu'].prefix),
            self.define('CMAKE_C_COMPILER', spec['llvm-amdgpu'].prefix.bin.clang)
        ]
