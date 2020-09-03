# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers,
       optimizers, and run-time environments."""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    url      = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='3e2542ce54b91b5c841f33d542143e0e43eae95e8785731405af29f08ace725b')
    version('3.5.0', sha256='4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('python', type='build')
    depends_on('z3', type='link')
    depends_on('zlib', type='link')
    depends_on('ncurses+termlib', type='link')

    # Will likely only be fixed in LLVM 12 upstream
    patch('fix-system-zlib-ncurses.patch')

    root_cmakelists_dir = 'llvm'

    install_targets = ['clang-tidy', 'install']

    @run_after('install')
    def create_wrapper_compiler(self):
        # Apparently renaming clang++ -> amdclang++ has the
        # side effect of it not working as a cxx compiler
        # anymore, so we copy the compilers to `bin/orig/`,
        # install the wrappers in `bin/`
        bin_dir = self.spec.prefix.bin
        orig_dir = bin_dir.orig
        mkdirp(orig_dir)

        bin_clang    = join_path(bin_dir, 'clang')
        bin_clangxx  = join_path(bin_dir, 'clang++')
        orig_clang   = join_path(orig_dir, 'clang')
        orig_clangxx = join_path(orig_dir, 'clang++')

        # Get the actual executable clang/clang++ refer to
        clang = os.readlink(bin_clang)
        if not os.path.isabs(clang):
            clang = join_path('..', clang)

        # Set up new symlinks to clang
        os.remove(bin_clang)
        os.remove(bin_clangxx)
        os.symlink(clang, orig_clang)
        os.symlink(clang, orig_clangxx)

        # Install the compiler wrapper in bin/
        package_dir = os.path.dirname(self.module.__file__)
        install(join_path(package_dir, 'cc'), bin_dir)
        os.symlink('cc', bin_clang)
        os.symlink('cc', bin_clangxx)

        # Replace $SPACK_CC and $SPACK_CXX with abs paths to clang
        cc = join_path(bin_dir, 'cc')
        filter_file(r'command\=\"\$SPACK_CC\"',
                    'command="{0}"'.format(orig_clang),
                    cc)
        filter_file(r'command\=\"\$SPACK_CXX\"',
                    'command="{0}"'.format(orig_clangxx),
                    cc)

    def cmake_args(self):
        args = [
            '-DLLVM_ENABLE_PROJECTS=clang;lld;clang-tools-extra;compiler-rt',
            '-DLLVM_ENABLE_ASSERTIONS=1'
        ]

        if self.compiler.name == "gcc":
            gcc_prefix = ancestor(self.compiler.cc, 2)
            args.append("-DGCC_INSTALL_PREFIX=" + gcc_prefix)

        return args
