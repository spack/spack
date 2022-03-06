# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# ispc requires <gnu/stubs-32.h>, e.g. from
# glibc-devel.i686 (CentoOS) or libc6-dev-i386 and g++-multilib (Ubuntu)


import re

from spack import *


class Ispc(CMakePackage):
    """Intel Implicit SPMD Program Compiler

    An open-source compiler for high-performance SIMD programming on the CPU"""

    homepage = "https://ispc.github.io"
    url      = "https://github.com/ispc/ispc/tarball/v1.14.1"
    git      = "https://github.com/ispc/ispc"
    maintainers = ['aumuell']

    executables = ['^ispc$']

    version('main', branch='main')
    version('1.17.0', sha256='1d47365febd2e17c84c22501aa63b1eafbc1ef826d6f5deadafe14783b8388a5')
    version('1.16.1', sha256='b32dbd374eea5f1b5f535bfd79c5cc35591c0df2e7bf1f86dec96b74e4ebf661')
    version('1.16.0', sha256='12db1a90046b51752a65f50426e1d99051c6d55e30796ddd079f7bc97d5f6faf')
    version('1.15.0', sha256='3b634aaa10c9bf0e82505d1af69cb307a3a00182d57eae019680ccfa62338af9')
    version('1.14.1', sha256='ca12f26dafbc4ef9605487d03a2156331c1351a4ffefc9bab4d896a466880794')
    version('1.14.0', sha256='1ed72542f56738c632bb02fb0dd56ad8aec3e2487839ebbc0def8334f305a4c7')
    version('1.13.0', sha256='aca595508b51dd1ff065c406a3fd7c93822320c510077dd4d97a2b98a23f097a')

    depends_on('python', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('ncurses', type='link')
    depends_on('zlib', type='link')
    depends_on('llvm+clang')
    depends_on('llvm@:12', when='@:1.16')
    depends_on('llvm@11:', when='@1.16.0:')
    depends_on('llvm@10:11', when='@1.15.0:1.15')
    depends_on('llvm@10.0:10', when='@1.13:1.14')

    patch('don-t-assume-that-ncurses-zlib-are-system-libraries.patch',
          when='@1.14.0:1.14',
          sha256='08cad761b6938fbb38a90b9dc2da1d85bf3cc77b0487cc31642a7a8549d52cab')

    patch('don-t-assume-that-ncurses-zlib-are-system-libraries-apple.patch',
          when='@1.14:',
          sha256='df7ad8a0fe3892c703a13a3d23e6587aaabbd600d3866836c32a2c22e3b2a0e9')

    patch('fix-linking-against-llvm-10.patch', when='@1.13.0:1.13',
          sha256='5ac4c25c871f08c62fe84ac6804f606d4080491c5676f9385b30f148c68b6c8a')

    def patch(self):
        with open("check-m32.c", "w") as f:
            f.write('#include <sys/cdefs.h>')
        try:
            Executable(self.compiler.cc)('-m32', '-shared', 'check-m32.c', error=str)
        except ProcessError:
            filter_file('bit 32 64', 'bit 64', 'cmake/GenerateBuiltins.cmake')

    def cmake_args(self):
        args = []
        # let CMake find NCurses, as ncurses it also in spec of llvm
        args.append('-DCURSES_NEED_NCURSES=TRUE')
        args.append('-DARM_ENABLED=FALSE')
        args.append('-DISPC_NO_DUMPS=ON')  # otherwise, LLVM needs patching
        args.append('-DISPC_INCLUDE_EXAMPLES=OFF')
        args.append('-DISPC_INCLUDE_TESTS=OFF')
        args.append('-DISPC_INCLUDE_UTILS=OFF')
        return args

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'^Intel.*[iI][sS][pP][cC]\),\s+(\S+)\s+\(build.*\)',
                          output)
        return match.group(1) if match else None
