# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack import *


class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers,
       optimizers, and run-time environments."""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    git      = "https://github.com/RadeonOpenCompute/llvm-project.git"
    url      = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='amd-stg-open')

    version('5.0.2', sha256='99a14394b406263576ed3d8d10334de7c78d42b349109f375d178b11492eecaf')
    version('5.0.0', sha256='bca2db4aaab71541cac588d6a708fde60f0ebe744809bde8a3847044a1a77413')
    version('4.5.2', sha256='36a4f7dd961cf373b743fc679bdf622089d2a905de2cfd6fd6c9e7ff8d8ad61f')
    version('4.5.0', sha256='b71451bf26650ba06c0c5c4c7df70f13975151eaa673ef0cc77c1ab0000ccc97')
    version('4.3.1', sha256='b53c6b13be7d77dc93a7c62e4adbb414701e4e601e1af2d1e98da4ee07c9837f')
    version('4.3.0', sha256='1567d349cd3bcd2c217b3ecec2f70abccd5e9248bd2c3c9f21d4cdb44897fc87')
    version('4.2.0', sha256='751eca1d18595b565cfafa01c3cb43efb9107874865a60c80d6760ba83edb661')
    version('4.1.0', sha256='244e38d824fa7dfa8d0edf3c036b3c84e9c17a16791828e4b745a8d31eb374ae', deprecated=True)
    version('4.0.0', sha256='aa1f80f429fded465e86bcfaef72255da1af1c5c52d58a4c979bc2f6c2da5a69', deprecated=True)
    version('3.10.0', sha256='8262aff88c1ff6c4deb4da5a4f8cda1bf90668950e2b911f93f73edaee53b370', deprecated=True)
    version('3.9.0', sha256='1ff14b56d10c2c44d36c3c412b190d3d8cd1bb12cfc7cd58af004c16fd9987d1', deprecated=True)
    version('3.8.0', sha256='93a28464a4d0c1c9f4ba55e473e5d1cde4c5c0e6d087ec8a0a3aef1f5f5208e8', deprecated=True)
    version('3.7.0', sha256='3e2542ce54b91b5c841f33d542143e0e43eae95e8785731405af29f08ace725b', deprecated=True)
    version('3.5.0', sha256='4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')
    variant('rocm-device-libs', default=True, description='Build ROCm device libs as external LLVM project instead of a standalone spack package.')
    variant('openmp', default=False, description='Enable OpenMP')
    variant(
        'llvm_dylib',
        default=False,
        description='Build LLVM shared library, containing all '
        'components in a single shared library',
    )
    variant(
        'link_llvm_dylib',
        default=False,
        description='Link LLVM tools against the LLVM shared library',
    )

    provides('libllvm@11', when='@3.5:3.8')
    provides('libllvm@12', when='@3.9:4.2')
    provides('libllvm@13', when='@4.3:')

    depends_on('cmake@3.4.3:',  type='build', when='@:3.8')
    depends_on('cmake@3.13.4:', type='build', when='@3.9.0:')
    depends_on('python', type='build')
    depends_on('z3', type='link')
    depends_on('zlib', type='link')
    depends_on('ncurses+termlib', type='link')

    # openmp dependencies
    depends_on("perl-data-dumper", type=("build"), when='+openmp')
    depends_on("hwloc", when='+openmp')
    depends_on('elf', type='link', when='+openmp')

    # Will likely only be fixed in LLVM 12 upstream
    patch('fix-system-zlib-ncurses.patch', when='@3.5.0:3.8.0')
    patch('fix-ncurses-3.9.0.patch', when='@3.9.0:4.0.0')

    # This is already fixed in upstream but not in 4.2.0 rocm release
    patch('fix-spack-detection-4.2.0.patch', when='@4.2.0:4.5.2')

    conflicts('^cmake@3.19.0')

    root_cmakelists_dir = 'llvm'
    install_targets = ['clang-tidy', 'install']

    # Add device libs sources so they can be an external LLVM project
    for d_version, d_shasum in [
        ('5.0.2',  '49cfa8f8fc276ba27feef40546788a2aabe259a924a97af8bef24e295d19aa5e'),
        ('5.0.0',  '83ed7aa1c9322b4fc1f57c48a63fc7718eb4195ee6fde433009b4bc78cb363f0'),
        ('4.5.2',  '50e9e87ecd6b561cad0d471295d29f7220e195528e567fcabe2ec73838979f61'),
        ('4.5.0',  '78412fb10ceb215952b5cc722ed08fa82501b5848d599dc00744ae1bdc196f77'),
        ('4.3.1',  'a7291813168e500bfa8aaa5d1dccf5250764ddfe27535def01b51eb5021d4592'),
        ('4.3.0',  '055a67e63da6491c84cd45865500043553fb33c44d538313dd87040a6f3826f2'),
        ('4.2.0',  '34a2ac39b9bb7cfa8175cbab05d30e7f3c06aaffce99eed5f79c616d0f910f5f'),
        ('4.1.0',  'f5f5aa6bfbd83ff80a968fa332f80220256447c4ccb71c36f1fbd2b4a8e9fc1b'),
        ('4.0.0',  'd0aa495f9b63f6d8cf8ac668f4dc61831d996e9ae3f15280052a37b9d7670d2a'),
        ('3.10.0', 'bca9291385d6bdc91a8b39a46f0fd816157d38abb1725ff5222e6a0daa0834cc'),
        ('3.9.0',  'c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7'),
        ('3.8.0',  'e82cc9a8eb7d92de02cabb856583e28f17a05c8cf9c97aec5275608ef1a38574'),
        ('3.7.0',  'b3a114180bf184b3b829c356067bc6a98021d52c1c6f9db6bc57272ebafc5f1d'),
        ('3.5.0',  'dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378')
    ]:
        resource(
            name='rocm-device-libs',
            placement='rocm-device-libs',
            url='https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-{0}.tar.gz'.format(d_version),
            sha256=d_shasum,
            when='@{0} +rocm-device-libs'.format(d_version)
        )

    resource(
        name='rocm-device-libs',
        placement='rocm-device-libs',
        git='https://github.com/RadeonOpenCompute/ROCm-Device-Libs.git',
        branch='amd-stg-open',
        when='@master +rocm-device-libs'
    )

    def cmake_args(self):
        llvm_projects = [
            'clang',
            'lld',
            'clang-tools-extra',
            'compiler-rt'
        ]
        args = []
        if self.spec.satisfies('@4.3.0:'):
            args = [
                self.define('LLVM_ENABLE_Z3_SOLVER', 'OFF'),
                self.define('LLLVM_ENABLE_ZLIB', 'ON'),
                self.define('CLANG_DEFAULT_LINKER', 'lld')
            ]
        if self.spec.satisfies('@4.3.0:4.5.2'):
            llvm_projects.append('libcxx')
            llvm_projects.append('libcxxabi')
            args.append(self.define('LIBCXX_ENABLE_SHARED', 'OFF'))
            args.append(self.define('LIBCXX_ENABLE_STATIC', 'ON'))
            args.append(self.define('LIBCXX_INSTALL_LIBRARY', 'OFF'))
            args.append(self.define('LIBCXX_INSTALL_HEADERS', 'OFF'))
            args.append(self.define('LIBCXXABI_ENABLE_SHARED', 'OFF'))
            args.append(self.define('LIBCXXABI_ENABLE_STATIC', 'ON'))
            args.append(self.define('LIBCXXABI_INSTALL_STATIC_LIBRARY', 'OFF'))

        if '+openmp' in self.spec:
            llvm_projects.append('openmp')

        args.extend([self.define('LLVM_ENABLE_PROJECTS', ';'.join(llvm_projects))])

        if self.spec.satisfies('@4.5.0:'):
            args.append(self.define('PACKAGE_VENDOR', 'AMD'))

        if self.spec.satisfies('@5.0.0:'):
            args.append(self.define('CLANG_ENABLE_AMDCLANG', 'ON'))

        # Enable rocm-device-libs as a external project
        if '+rocm-device-libs' in self.spec:
            dir = os.path.join(self.stage.source_path, 'rocm-device-libs')
            args.extend([
                self.define('LLVM_EXTERNAL_PROJECTS', 'device-libs'),
                self.define('LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR', dir)
            ])

        if '+llvm_dylib' in self.spec:
            args.append("-DLLVM_BUILD_LLVM_DYLIB:Bool=ON")

        if '+link_llvm_dylib' in self.spec:
            args.append("-DLLVM_LINK_LLVM_DYLIB:Bool=ON")

        # Get the GCC prefix for LLVM.
        if self.compiler.name == "gcc":
            compiler = Executable(self.compiler.cc)
            gcc_output = compiler('-print-search-dirs', output=str, error=str)

            gcc_prefix = ""
            for line in gcc_output.splitlines():
                if line.startswith("install:"):
                    # Get path and strip any whitespace
                    # (causes oddity with ancestor)
                    gcc_prefix = line.split(":")[1].strip()
                    gcc_prefix = ancestor(gcc_prefix, 4)
                    break
            args.append(self.define('GCC_INSTALL_PREFIX', gcc_prefix))

        return args

    @run_after("install")
    def post_install(self):
        # TODO:Enabling LLVM_ENABLE_RUNTIMES for libcxx,libcxxabi did not build.
        # bootstraping the libcxx with the just built clang
        if self.spec.satisfies('@4.5.0:'):
            spec = self.spec
            define = CMakePackage.define
            libcxxdir = "build-bootstrapped-libcxx"
            with working_dir(libcxxdir, create=True):
                cmake_args = [
                    self.stage.source_path + "/libcxx",
                    define("CMAKE_C_COMPILER", spec.prefix.bin + "/clang"),
                    define("CMAKE_CXX_COMPILER", spec.prefix.bin + "/clang++"),
                    define("CMAKE_INSTALL_PREFIX", spec.prefix),
                ]
                cmake_args.extend(self.cmake_args())
                cmake(*cmake_args)
                make()
