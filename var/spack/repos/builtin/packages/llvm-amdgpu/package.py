# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers,
       optimizers, and run-time environments."""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    url      = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('python', type='build')
    depends_on('z3', type='link')
    depends_on('zlib', type='link')
    depends_on('ncurses+termlib', type='link')

    patch('fix-system-zlib-ncurses.patch')

    root_cmakelists_dir = 'llvm'

    install_targets = ['clang-tidy', 'install']

    def cmake_args(self):
        args = [
            '-DLLVM_ENABLE_PROJECTS=clang;lld;clang-tools-extra;compiler-rt',
            '-DLLVM_ENABLE_ASSERTIONS=1'
        ]

        if self.compiler.name == "gcc":
            gcc_prefix = ancestor(self.compiler.cc, 2)
            args.append("-DGCC_INSTALL_PREFIX=" + gcc_prefix)

        return args
