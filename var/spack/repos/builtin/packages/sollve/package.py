# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sollve(CMakePackage):
    """The SOLLVE Project aims at scaling OpenMP by leveraging LLVM for exascale
       performance and portability of applications.  This package provides a
       collection of Clang/LLVM compilers and an OpenMP runtime library.
    """

    homepage = 'https://www.bnl.gov/compsci/projects/SOLLVE/'
    url      = "https://github.com/SOLLVE"

    family = 'compiler'  # Used by lmod

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant('clang', default=True,
            description="Build the LLVM C/C++/Objective-C compiler frontend")
    variant('lldb', default=True, description="Build the LLVM debugger")
    variant('lld', default=True, description="Build the LLVM linker")
    variant('internal_unwind', default=True,
            description="Build the libcxxabi libunwind")
    variant('polly', default=True,
            description="Build the LLVM polyhedral optimization plugin, "
            "only builds for 3.7.0+")
    variant('libcxx', default=True,
            description="Build the LLVM C++ standard library")
    variant('compiler-rt', default=True,
            description="Build LLVM compiler runtime, including sanitizers")
    variant('gold', default=True,
            description="Add support for LTO with the gold linker plugin")
    variant('shared_libs', default=False,
            description="Build all components as shared libraries, faster, "
            "less memory to build, less stable")
    variant('link_dylib', default=False,
            description="Build and link the libLLVM shared library rather "
            "than static")
    variant('all_targets', default=False,
            description="Build all supported targets, default targets "
            "<current arch>,NVPTX,AMDGPU,CppBackend")
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('omp_tsan', default=False,
            description="Build with OpenMP capable thread sanitizer")
    variant('python', default=False, description="Install python bindings")
    variant('argobots', default=True, description="Use Argobots in BOLT")
    extends('python', when='+python')

    # Build dependency
    depends_on('cmake@3.4.3:', type='build')
    depends_on('python', when='~python', type='build')

    # Universal dependency
    depends_on('python')

    # openmp dependencies
    depends_on('perl-data-dumper', type=('build'))
    depends_on('argobots', when='+argobots')

    # lldb dependencies
    depends_on('ncurses', when='+lldb')
    depends_on('swig', when='+lldb')
    depends_on('libedit', when='+lldb')
    depends_on('py-six', when='+lldb +python')

    # gold support
    depends_on('binutils+gold', when='+gold')

    version("develop", git='https://github.com/SOLLVE/llvm.git')
    resource(name='compiler-rt',
             svn='http://llvm.org/svn/llvm-project/compiler-rt/trunk',
             destination='projects', when='@develop+compiler-rt',
             placement='compiler-rt')
    resource(name='openmp', git='https://github.com/pmodels/bolt.git',
             destination='projects', when='@develop+clang', placement='openmp')
    resource(name='polly', git='https://github.com/SOLLVE/polly.git',
             destination='tools', when='@develop+polly', placement='polly')
    resource(name='libcxx', git='https://github.com/SOLLVE/libcxx.git',
             destination='projects', when='@develop+libcxx',
             placement='libcxx')
    resource(name='libcxxabi', git='https://github.com/SOLLVE/libcxxabi.git',
             destination='projects', when='@develop+libcxx',
             placement='libcxxabi')
    resource(name='cfe', git='https://github.com/SOLLVE/clang.git',
             destination='tools', when='@develop+clang', placement='clang')
    resource(name='lldb', svn='http://llvm.org/svn/llvm-project/lldb/trunk',
             destination='tools', when='@develop+lldb', placement='lldb')
    resource(name='lld', svn='http://llvm.org/svn/llvm-project/lld/trunk',
             destination='tools', when='@develop+lld', placement='lld')
    resource(name='libunwind',
             svn='http://llvm.org/svn/llvm-project/libunwind/trunk',
             destination='projects', when='@develop+internal_unwind',
             placement='libunwind')

    conflicts('+clang_extra', when='~clang')
    conflicts('+lldb',        when='~clang')

    conflicts('%gcc@:5.0.999')
    conflicts('+omp_tsan')

    @run_before('cmake')
    def check_darwin_lldb_codesign_requirement(self):
        if not self.spec.satisfies('+lldb platform=darwin'):
            return
        codesign = which('codesign')
        mkdir('tmp')
        llvm_check_file = join_path('tmp', 'llvm_check')
        copy('/usr/bin/false', llvm_check_file)

        try:
            codesign('-f', '-s', 'lldb_codesign', '--dryrun',
                     llvm_check_file)

        except ProcessError:
            explanation = ('The "lldb_codesign" identity must be available'
                           ' to build LLVM with LLDB. See https://llvm.org/'
                           'svn/llvm-project/lldb/trunk/docs/code-signing'
                           '.txt for details on how to create this identity.')
            raise RuntimeError(explanation)

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.compiler.cxx11_flag)

        if '+clang' in self.spec:
            run_env.set('CC', join_path(self.spec.prefix.bin, 'clang'))
            run_env.set('CXX', join_path(self.spec.prefix.bin, 'clang++'))

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_EH:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
            '-DPYTHON_EXECUTABLE:PATH={0}'.format(spec['python'].command.path),
        ]

        # TODO: Instead of unconditionally disabling CUDA, add a "cuda" variant
        #       (see TODO above), and set the paths if enabled.
        cmake_args.extend([
            '-DCUDA_TOOLKIT_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_SDK_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_NVCC_EXECUTABLE:FILEPATH=IGNORE',
            '-DLIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES:STRING=IGNORE'])

        if '+gold' in spec:
            cmake_args.append('-DLLVM_BINUTILS_INCDIR=' +
                              spec['binutils'].prefix.include)
        if '+polly' in spec:
            cmake_args.append('-DLINK_POLLY_INTO_TOOLS:Bool=ON')
        else:
            cmake_args.extend(['-DLLVM_EXTERNAL_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_TOOL_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_POLLY_LINK_INTO_TOOLS:Bool=OFF'])

        if '+python' in spec and '+lldb' in spec:
            cmake_args.append('-DLLDB_USE_SYSTEM_SIX:Bool=TRUE')
        if '+clang' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_CLANG_BUILD:Bool=OFF')
        if '+lldb' not in spec:
            cmake_args.extend(['-DLLVM_EXTERNAL_LLDB_BUILD:Bool=OFF',
                               '-DLLVM_TOOL_LLDB_BUILD:Bool=OFF'])
        if '+lld' not in spec:
            cmake_args.append('-DLLVM_TOOL_LLD_BUILD:Bool=OFF')
        if '+internal_unwind' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_LIBUNWIND_BUILD:Bool=OFF')
        if '+libcxx' in spec:
            cmake_args.append('-DCLANG_DEFAULT_CXX_STDLIB=libc++')
        else:
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXX_BUILD:Bool=OFF')
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXXABI_BUILD:Bool=OFF')
        if '+compiler-rt' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_COMPILER_RT_BUILD:Bool=OFF')

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')

        if '+link_dylib' in spec:
            cmake_args.append('-DLLVM_LINK_LLVM_DYLIB:Bool=ON')

        if '+all_targets' not in spec:  # all is default on cmake
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
                '-DLLVM_TARGETS_TO_BUILD:STRING=' + ';'.join(targets))

        if '+omp_tsan' in spec:
            cmake_args.append('-DLIBOMP_TSAN_SUPPORT=ON')

        if '+argobots' in spec:
            cmake_args.extend([
                '-DLIBOMP_USE_ITT_NOTIFY=off',
                '-DLIBOMP_USE_ARGOBOTS=on',
                '-DLIBOMP_ARGOBOTS_INSTALL_DIR=' + spec['argobots'].prefix])

        if self.compiler.name == 'gcc':
            gcc_prefix = ancestor(self.compiler.cc, 2)
            cmake_args.append('-DGCC_INSTALL_PREFIX=' + gcc_prefix)

        if spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return cmake_args

    @run_before('build')
    def pre_install(self):
        with working_dir(self.build_directory):
            # When building shared libraries these need to be installed first
            make('install-LLVMTableGen')
            if self.spec.version >= Version('4.0.0'):
                # LLVMDemangle target was added in 4.0.0
                make('install-LLVMDemangle')
            make('install-LLVMSupport')

    @run_after('install')
    def post_install(self):
        if '+clang' in self.spec and '+python' in self.spec:
            install_tree(
                'tools/clang/bindings/python/clang',
                join_path(site_packages_dir, 'clang'))

        with working_dir(self.build_directory):
            install_tree('bin', join_path(self.prefix, 'libexec', 'llvm'))
