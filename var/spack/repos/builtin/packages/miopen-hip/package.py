# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MiopenHip(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpen"
    url = "https://github.com/ROCmSoftwarePlatform/MIOpen/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='aa362e69c4dce7f5751f0ee04c745735ea5454c8101050e9b92cc60fa3c0fb82')

    variant('build_type', default='Release', description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('boost@1.58.0', type='link')
    depends_on('pkg-config', type='build')
    depends_on('bzip2', type='link')
    depends_on('sqlite', type='link')
    depends_on('half', type='build')
    for ver in ['3.5.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='link', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-clang-ocl@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        args = [
            '-DMIOPEN_BACKEND=HIP',
            '-DCMAKE_CXX_COMPILER={}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix),
            '-DBoost_USE_STATIC_LIBS=Off'
        ]
        return args
