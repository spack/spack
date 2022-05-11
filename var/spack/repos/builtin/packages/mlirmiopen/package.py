# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mlirmiopen(CMakePackage):
    """Multi-Level Intermediate Representation for rocm miopen project."""

    homepage = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir"
    url = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir/archive/release/rocm-5.1.0.tar.gz"
    git = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir.git"

    maintainers = ['srekolam']
    version('5.1.0', sha256='43af5f131bd688c00250fd60ac51f175ed9ce84af5dc72365ea8108dccbaf583')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('python', type='build')
    depends_on('z3', type='link')
    depends_on('zlib', type='link')
    depends_on('ncurses+termlib', type='link')
    depends_on('bzip2')
    depends_on('sqlite')
    depends_on('half')
    depends_on('pkgconfig', type='build')

    for ver in ['5.1.0']:
        depends_on('hip@' + ver,                       when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,               when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver,               when='@' + ver)
        depends_on('rocm-cmake@' + ver,  type='build', when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        llvm_projects = [
            'mlir',
            'lld'
        ]
        args = [
            self.define(
                'CMAKE_CXX_COMPILER',
                '{0}/bin/clang++'.format(spec['llvm-amdgpu'].prefix)
            ),
            self.define(
                'CMAKE_C_COMPILER',
                '{0}/bin/clang'.format(spec['llvm-amdgpu'].prefix)
            ),
            self.define('HIP_PATH', spec['hip'].prefix),
            self.define('BUILD_FAT_LIBMLIRMIOPEN', 'ON')
        ]
        args.extend([self.define('LLVM_ENABLE_PROJECTS', ';'.join(llvm_projects))])
        return args
