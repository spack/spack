# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers, optimizers, and run-time environments."""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    url      = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2', type='build')

    root_cmakelists_dir = 'llvm'

    install_targets = ['clang-tidy', 'install']

    def cmake_args(self):
        args = [
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DLLVM_ENABLE_PROJECTS=clang;lld;clang-tools-extra;compiler-rt',
                '-DLLVM_ENABLE_ASSERTIONS=1'
               ]
        return args

