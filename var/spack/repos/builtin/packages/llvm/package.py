# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Llvm(CMakePackage):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = 'http://llvm.org/'
    url      = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    list_url = 'http://releases.llvm.org/download.html'
    git      = 'https://github.com/llvm/llvm-project'

    family = 'compiler'  # Used by lmod

    version('master', branch='master')
    version('9.0.1', sha256='be7b034641a5fda51ffca7f5d840b1a768737779f75f7c4fd18fe2d37820289a')
    version('9.0.0', sha256='7807fac25330e24e9955ca46cd855dd34bbc9cc4fdba8322366206654d1036f2')
    version('8.0.0', sha256='d81238b4a69e93e29f74ce56f8107cbfcf0c7d7b40510b7879e98cc031e25167')
    version('7.1.0', sha256='71c93979f20e01f1a1cc839a247945f556fa5e63abf2084e8468b238080fd839')
    version('7.0.1', sha256='f17a6cd401e8fd8f811fbfbb36dcb4f455f898c9d03af4044807ad005df9f3c0')
    version('6.0.1', sha256='aefadceb231f4c195fe6d6cd3b1a010b269c8a22410f339b5a089c2e902aa177')
    version('6.0.0', sha256='1946ec629c88d30122afa072d3c6a89cc5d5e4e2bb28dc63b2f9ebcc7917ee64')
    version('5.0.2', sha256='fe87aa11558c08856739bfd9bd971263a28657663cb0c3a0af01b94f03b0b795')
    version('5.0.1', sha256='84ca454abf262579814a2a2b846569f6e0cb3e16dc33ca3642b4f1dff6fbafd3')
    version('5.0.0', sha256='1f1843315657a4371d8ca37f01265fa9aae17dbcf46d2d0a95c1fdb3c6a4bab6')
    version('4.0.1', sha256='cd664fb3eec3208c08fb61189c00c9118c290b3be5adb3215a97b24255618be5')
    version('4.0.0', sha256='28ca4b2fc434cb1f558e8865386c233c2a6134437249b8b3765ae745ffa56a34')
    version('3.9.1', sha256='f5b6922a5c65f9232f83d89831191f2c3ccf4f41fdd8c63e6645bbf578c4ab92')
    version('3.9.0', sha256='9c6563a72c8b5b79941c773937d997dd2b1b5b3f640136d02719ec19f35e0333')
    version('3.8.1', sha256='69360f0648fde0dc3d3c4b339624613f3bc2a89c4858933bc3871a250ad02826')
    version('3.8.0', sha256='b5cc5974cc2fd4e9e49e1bbd0700f872501a8678bd9694fa2b36c65c026df1d1')
    version('3.7.1', sha256='d2cb0eb9b8eb21e07605bfe5e7a5c6c5f5f8c2efdac01ec1da6ffacaabe4195a')
    version('3.7.0', sha256='dc00bc230be2006fb87b84f6fe4800ca28bc98e6692811a98195da53c9cb28c6')
    version('3.6.2', sha256='f75d703a388ba01d607f9cf96180863a5e4a106827ade17b221d43e6db20778a')
    version('3.5.1', sha256='5d739684170d5b2b304e4fb521532d5c8281492f71e1a8568187bfa38eb5909d')

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant('clang', default=True,
            description="Build the LLVM C/C++/Objective-C compiler frontend")

    # TODO: The current version of this package unconditionally disables CUDA.
    #       Better would be to add a "cuda" variant that:
    #        - Adds dependency on the "cuda" package when enabled
    #        - Sets the necessary CMake flags when enabled
    #        - Disables CUDA (as this current version does) only when the
    #          variant is also disabled.

    # variant('cuda', default=False,
    #         description="Build the LLVM with CUDA features enabled")

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
    variant('gold', default=(sys.platform != 'darwin'),
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

    extends('python', when='+python')

    # Build dependency
    depends_on('cmake@3.4.3:', type='build')
    depends_on('python@2.7:2.8', when='@:4.999 ~python', type='build')
    depends_on('python', when='@5: ~python', type='build')

    # Universal dependency
    depends_on('python@2.7:2.8', when='@:4.999+python')
    depends_on('python', when='@5:+python')

    # openmp dependencies
    depends_on('perl-data-dumper', type=('build'))

    # ncurses dependency
    depends_on('ncurses+termlib')

    # lldb dependencies
    depends_on('swig', when='+lldb')
    depends_on('libedit', when='+lldb')
    depends_on('py-six', when='@5.0.0: +lldb +python')

    # gold support
    depends_on('binutils+gold', when='+gold')

    # polly plugin
    depends_on('gmp', when='@:3.6.999 +polly')
    depends_on('isl', when='@:3.6.999 +polly')

    conflicts('+clang_extra',     when='~clang')
    conflicts('+lldb',            when='~clang')
    conflicts('+libcxx',          when='~clang')
    conflicts('+internal_unwind', when='~clang')
    conflicts('+compiler-rt',     when='~clang')

    # LLVM 4 and 5 does not build with GCC 8
    conflicts('%gcc@8:',       when='@:5')
    conflicts('%gcc@:5.0.999', when='@8:')

    # OMP TSAN exists in > 5.x
    conflicts('+omp_tsan', when='@:5.99')

    # Github issue #4986
    patch('llvm_gcc7.patch', when='@4.0.0:4.0.1+lldb %gcc@7.0:')
    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch('constexpr_longdouble.patch', when='@6:8+libcxx')
    patch('constexpr_longdouble_9.0.patch', when='@9+libcxx')

    # Backport from llvm master; see
    # https://bugs.llvm.org/show_bug.cgi?id=38233
    # for a bug report about this problem in llvm master.
    patch('llvm_py37.patch', when='@4:6 ^python@3.7:')

    # https://bugs.llvm.org/show_bug.cgi?id=39696
    patch('thread-p9.patch', when='@develop+libcxx')

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
            # Newer LLVM versions have a simple script that sets up
            # automatically
            setup = Executable("./lldb/scripts/macos-setup-codesign.sh")
            try:
                setup()
            except Exception:
                raise RuntimeError(
                    'The "lldb_codesign" identity must be available to build '
                    'LLVM with LLDB. See https://lldb.llvm.org/resources/'
                    'build.html#code-signing-on-macos for details on how to '
                    'create this identity.'
                )

    def setup_build_environment(self, env):
        env.append_flags('CXXFLAGS', self.compiler.cxx11_flag)

    def setup_run_environment(self, env):
        if '+clang' in self.spec:
            env.set('CC', join_path(self.spec.prefix.bin, 'clang'))
            env.set('CXX', join_path(self.spec.prefix.bin, 'clang++'))

    root_cmakelists_dir = 'llvm'

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_EH:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
            '-DPYTHON_EXECUTABLE:PATH={0}'.format(spec['python'].command.path),
        ]

        projects = []

        # TODO: Instead of unconditionally disabling CUDA, add a "cuda" variant
        #       (see TODO above), and set the paths if enabled.
        cmake_args.extend([
            '-DCUDA_TOOLKIT_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_SDK_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_NVCC_EXECUTABLE:FILEPATH=IGNORE',
            '-DLIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES:STRING=IGNORE'])

        if '+python' in spec and '+lldb' in spec and spec.satisfies('@5.0.0:'):
            cmake_args.append('-DLLDB_USE_SYSTEM_SIX:Bool=TRUE')

        if '~python' in spec and '+lldb' in spec:
            cmake_args.append('-DLLDB_DISABLE_PYTHON:Bool=TRUE')

        if '+gold' in spec:
            cmake_args.append('-DLLVM_BINUTILS_INCDIR=' +
                              spec['binutils'].prefix.include)

        if '+clang' in spec:
            projects.append('clang')
            projects.append('clang-tools-extra')
            projects.append('openmp')
        if '+lldb' in spec:
            projects.append('lldb')
        if '+lld' in spec:
            projects.append('lld')
        if '+compiler-rt' in spec:
            projects.append('compiler-rt')
        if '+libcxx' in spec:
            projects.append('libcxx')
            projects.append('libcxxabi')
            if spec.satisfies('@3.9.0:'):
                cmake_args.append('-DCLANG_DEFAULT_CXX_STDLIB=libc++')
        if '+internal_unwind' in spec:
            projects.append('libunwind')
        if '+polly' in spec:
            projects.append('polly')
            cmake_args.append('-DLINK_POLLY_INTO_TOOLS:Bool=ON')

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')

        if '+link_dylib' in spec:
            cmake_args.append('-DLLVM_LINK_LLVM_DYLIB:Bool=ON')

        if '+all_targets' not in spec:  # all is default on cmake

            targets = ['NVPTX', 'AMDGPU']
            if (spec.version < Version('3.9.0')):
                # Starting in 3.9.0 CppBackend is no longer a target (see
                # LLVM_ALL_TARGETS in llvm's top-level CMakeLists.txt for
                # the complete list of targets)
                targets.append('CppBackend')

            if spec.target.family == 'x86' or spec.target.family == 'x86_64':
                targets.append('X86')
            elif spec.target.family == 'arm':
                targets.append('ARM')
            elif spec.target.family == 'aarch64':
                targets.append('AArch64')
            elif (spec.target.family == 'sparc' or
                  spec.target.family == 'sparc64'):
                targets.append('Sparc')
            elif (spec.target.family == 'ppc64' or
                  spec.target.family == 'ppc64le' or
                  spec.target.family == 'ppc' or
                  spec.target.family == 'ppcle'):
                targets.append('PowerPC')

            cmake_args.append(
                '-DLLVM_TARGETS_TO_BUILD:STRING=' + ';'.join(targets))

        if '+omp_tsan' in spec:
            cmake_args.append('-DLIBOMP_TSAN_SUPPORT=ON')

        if self.compiler.name == 'gcc':
            gcc_prefix = ancestor(self.compiler.cc, 2)
            cmake_args.append('-DGCC_INSTALL_PREFIX=' + gcc_prefix)

        if spec.satisfies('@4.0.0:'):
            if spec.satisfies('platform=cray') or \
               spec.satisfies('platform=linux'):
                cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')

        # Semicolon seperated list of projects to enable
        cmake_args.append(
            '-DLLVM_ENABLE_PROJECTS:STRING={0}'.format(';'.join(projects)))

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
        if '+python' in self.spec:
            install_tree('llvm/bindings/python', site_packages_dir)

            if '+clang' in self.spec:
                install_tree('clang/bindings/python', site_packages_dir)

        with working_dir(self.build_directory):
            install_tree('bin', join_path(self.prefix, 'libexec', 'llvm'))
