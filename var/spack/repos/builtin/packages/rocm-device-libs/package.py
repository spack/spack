# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs"
    git      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs.git"
    url      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='amd-stg-open')

    version('5.1.0', sha256='47dbcb41fb4739219cadc9f2b5f21358ed2f9895ce786d2f7a1b2c4fd044d30f')
    version('5.0.2', sha256='49cfa8f8fc276ba27feef40546788a2aabe259a924a97af8bef24e295d19aa5e')
    version('5.0.0', sha256='83ed7aa1c9322b4fc1f57c48a63fc7718eb4195ee6fde433009b4bc78cb363f0')
    version('4.5.2', sha256='50e9e87ecd6b561cad0d471295d29f7220e195528e567fcabe2ec73838979f61')
    version('4.5.0', sha256='78412fb10ceb215952b5cc722ed08fa82501b5848d599dc00744ae1bdc196f77')
    version('4.3.1', sha256='a7291813168e500bfa8aaa5d1dccf5250764ddfe27535def01b51eb5021d4592')
    version('4.3.0', sha256='055a67e63da6491c84cd45865500043553fb33c44d538313dd87040a6f3826f2')
    version('4.2.0', sha256='34a2ac39b9bb7cfa8175cbab05d30e7f3c06aaffce99eed5f79c616d0f910f5f')
    version('4.1.0', sha256='f5f5aa6bfbd83ff80a968fa332f80220256447c4ccb71c36f1fbd2b4a8e9fc1b', deprecated=True)
    version('4.0.0', sha256='d0aa495f9b63f6d8cf8ac668f4dc61831d996e9ae3f15280052a37b9d7670d2a', deprecated=True)
    version('3.10.0', sha256='bca9291385d6bdc91a8b39a46f0fd816157d38abb1725ff5222e6a0daa0834cc', deprecated=True)
    version('3.9.0', sha256='c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7', deprecated=True)
    version('3.8.0', sha256='e82cc9a8eb7d92de02cabb856583e28f17a05c8cf9c97aec5275608ef1a38574', deprecated=True)
    version('3.7.0', sha256='b3a114180bf184b3b829c356067bc6a98021d52c1c6f9db6bc57272ebafc5f1d', deprecated=True)
    version('3.5.0', sha256='dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('zlib', type='link', when='@3.9.0:')
    depends_on('texinfo', type='link', when='@3.9.0:')

    # Make sure llvm is not built with rocm-device-libs (that is, it's already
    # built with rocm-device-libs as an external project).
    depends_on('llvm-amdgpu ~rocm-device-libs')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', 'master']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,              when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        return [
            self.define('LLVM_DIR', spec['llvm-amdgpu'].prefix),
            self.define('CMAKE_C_COMPILER', spec['llvm-amdgpu'].prefix.bin.clang)
        ]
