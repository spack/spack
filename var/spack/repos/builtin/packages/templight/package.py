##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Templight(CMakePackage):
    """Templight is a Clang-based tool to profile the time and memory
       consumption of template instantiations and to perform interactive
       debugging sessions to gain introspection into the template
       instantiation process."""

    homepage = "https://github.com/mikael-s-persson/templight"
    git      = "https://github.com/mikael-s-persson/templight.git"
    llvm_svn = "http://llvm.org/svn/llvm-project/{0}/trunk"

    family = 'compiler'  # Used by lmod

    # Templight is a patch to clang, so we have three versions to care about:
    # - The one that will be used in Spack specifications
    # - The git branch that we need to fetch from in the templight repo
    # - The svn tag that we need to fetch from in the LLVM repos
    version('develop', branch='master')
    resource(name='llvm-trunk',
             svn=llvm_svn.format('llvm'),
             destination='.',
             placement='llvm',
             when='@develop')
    resource(name='clang-trunk',
             svn=llvm_svn.format('cfe'),
             destination='llvm/tools',
             placement='clang',
             when='@develop')

    # Templight has no stable release yet, and is supposed to be built against
    # the LLVM trunk. As this is a brittle combination, I decided to
    # artificially create a stable release based on what works today. Please
    # feel free to remove this version once templight has stabilized.
    version('2018.07.20', commit='91589f95427620dd0a2346bd69ba922f374aa42a')
    resource(name='llvm-r337566',
             svn=llvm_svn.format('llvm'),
             revision=337566,
             destination='.',
             placement='llvm',
             when='@2018.07.20')
    resource(name='clang-r337566',
             svn=llvm_svn.format('cfe'),
             revision=337566,
             destination='llvm/tools',
             placement='clang',
             when='@2018.07.20')
    patch('develop-20180720.patch', when='@2018.07.20')

    # Clang debug builds can be _huge_ (20+ GB), make sure you know what you
    # are doing before switching to them
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # NOTE: LLVM has many configurable tweaks and optional tools/extensions.
    #       I did not think that  propagating all of these to a debugging and
    #       performance analysis tool was worth the maintenance burden. But
    #       if you disagree, the llvm package can be used for inspiration.

    depends_on('cmake@3.4.3:', type='build')
    depends_on('python')
    depends_on('py-lit', type=('build', 'run'))

    def patch(self):
        # We start with the templight source tree and an "llvm" subdir.
        # But we actually need an llvm source tree with a "templight" subdir.
        # Let's flip the directory organization around
        templight_files = os.listdir('.')
        templight_files.remove('llvm')
        templight_dir = 'llvm/tools/clang/tools/templight'
        os.mkdir(templight_dir)
        for name in templight_files:
            os.rename(name, os.path.join(templight_dir, name))
        for name in os.listdir('llvm'):
            os.rename(os.path.join('llvm', name), name)
        os.rmdir('llvm')

        # Tell the clang build system that it needs to build templight
        with open("tools/clang/tools/CMakeLists.txt", "a") as cmake_lists:
            cmake_lists.write("add_clang_subdirectory(templight)")

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.compiler.cxx11_flag)
        run_env.set('CC', join_path(self.spec.prefix.bin, 'templight'))
        run_env.set('CXX', join_path(self.spec.prefix.bin, 'templight++'))

    def cmake_args(self):
        spec = self.spec

        # Templight is a debugging tool, not a production compiler, so we only
        # need a very bare-bones build of clang
        #
        # Minimal build config ideas were taken from the llvm package, with
        # the templight-specific assumption that we will always be building
        # for LLVM / Clang 5.0+ and can safely ignore older tricks.
        #
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
            '-DPYTHON_EXECUTABLE:PATH={0}'.format(spec['python'].command.path),
            '-DLLVM_EXTERNAL_POLLY_BUILD:Bool=OFF',
            '-DLLVM_TOOL_POLLY_BUILD:Bool=OFF',
            '-DLLVM_POLLY_BUILD:Bool=OFF',
            '-DLLVM_POLLY_LINK_INTO_TOOLS:Bool=OFF',
            '-DLLVM_EXTERNAL_LLDB_BUILD:Bool=OFF',
            '-DLLVM_TOOL_LLDB_BUILD:Bool=OFF',
            '-DLLVM_TOOL_LLD_BUILD:Bool=OFF',
            '-DLLVM_EXTERNAL_LIBUNWIND_BUILD:Bool=OFF',
            '-DLLVM_EXTERNAL_LIBCXX_BUILD:Bool=OFF',
            '-DLLVM_EXTERNAL_LIBCXXABI_BUILD:Bool=OFF',
            '-DLLVM_EXTERNAL_COMPILER_RT_BUILD:Bool=OFF',
        ]

        targets = ['NVPTX', 'AMDGPU']

        if 'x86' in spec.architecture.target.lower():
            targets.append('X86')
        elif 'arm' in spec.architecture.target.lower():
            targets.append('ARM')
        elif 'aarch64' in spec.architecture.target.lower():
            targets.append('AArch64')
        elif 'sparc' in spec.architecture.target.lower():
            targets.append('Sparc')
        elif ('ppc' in spec.architecture.target.lower() or
              'power' in spec.architecture.target.lower()):
            targets.append('PowerPC')

        cmake_args.append(
            '-DLLVM_TARGETS_TO_BUILD:Bool=' + ';'.join(targets))

        if spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')

        return cmake_args

    @run_after('install')
    def post_install(self):
        with working_dir(self.build_directory):
            install_tree('bin', self.prefix.libexec.llvm)
