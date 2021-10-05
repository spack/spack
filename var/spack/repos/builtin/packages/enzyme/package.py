
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Enzyme(CMakePackage):
    """
    The Enzyme project is a tool for performing reverse-mode automatic
    differentiation (AD) of statically-analyzable LLVM IR.
    This allows developers to use Enzyme to automatically create gradients
    of their source code without much additional work.
    """

    homepage = "https://enzyme.mit.edu"
    url      = "https://github.com/wsmoses/Enzyme/archive/v0.0.15.tar.gz"
    list_url = "https://github.com/wsmoses/Enzyme/releases"
    git      = "https://github.com/wsmoses/Enzyme"

    maintainers = ['wsmoses', 'vchuravy', 'tgymnich']

    root_cmakelists_dir = 'enzyme'

    version('main', branch='main')
    version('0.0.15',
            sha256='1ec27db0d790c4507b2256d851b256bf7e074eec933040e9e375d6e352a3c159')
    version('0.0.14',
            sha256='740641eeeeadaf47942ac88cc52e62ddc0e8c25767a501bed36ec241cf258b8d')
    version('0.0.13',
            sha256='d4a53964ec1f763772db2c56e6734269b7656c8b2ecd41fa7a41315bcd896b5a')

    variant(
        'build_type',
        default='Release',
        description='CMake build type',
        values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel')
    )

    depends_on('llvm@7:12')
    depends_on('cmake@3.9:', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DLLVM_DIR=" + spec["llvm"].prefix.lib + "/cmake/llvm"
        ]
        return args

    @property
    def libs(self):
        ver = self.spec['llvm'].version.up_to(1)
        libs = [
            'LLVMEnzyme-{0}'.format(ver),
            'ClangEnzyme-{0}'.format(ver)
        ]
        return find_libraries(libs, root=self.prefix, recursive=True)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Get the LLVMEnzyme and ClangEnzyme lib paths
        llvm, clang = self.libs

        if "LLVMEnzyme-" in clang:
            llvm, clang = clang, llvm

        env.set('LLVMENZYME', llvm)
        env.set('CLANGENZYME', clang)
