# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LlvmFlang(CMakePackage, CudaPackage):
    """LLVM-Flang is the Flang fork of LLVM needed by the Flang package."""

    homepage = "https://github.com/flang-compiler"

    git      = "https://github.com/flang-compiler/llvm.git"

    maintainer = ['naromero77']

    version('master', branch='master')
    version('release_70', branch='release_70')
    version('release_60', branch='release_60')
    version('20190329', tag='flang_20190329')
    version('20181226_70', tag='20181226_70')
    version('20181226_60', tag='20181226_60')
    version('20180921', tag='20180921')
    version('20180319', tag='20180319')
    version('20180328', tag='20180308')

    # Variants
    variant('all_targets', default=False,
            description='Build all supported targets')

    variant('build_type', default='Release',
            description='The CMake build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # Universal dependency
    depends_on('cmake@3.8:', type='build')
    depends_on('python@2.7:', type='build')

    # openmp dependencies
    depends_on('perl-data-dumper', type=('build'))
    depends_on('hwloc')

    # libomptarget dependencies
    depends_on('libelf', when='+cuda')
    depends_on('libffi', when='+cuda')
    depends_on('cuda@:9', when='+cuda')  # llvm 7 not compatible with newer version of cuda

    # LLVM-Flang Componentes: Driver, OpenMP
    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='master',
             destination='tools',
             placement='clang',
             when='@master')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='release_70',
             destination='tools',
             placement='clang',
             when='@release_70')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='release_60',
             destination='tools',
             placement='clang',
             when='@release_60')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20190329',
             destination='tools',
             placement='clang',
             when='@20190329')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20181226_70',
             destination='tools',
             placement='clang',
             when='@20181226_70')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20181226_60',
             destination='tools',
             placement='clang',
             when='@20181226_60')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20180921',
             destination='tools',
             placement='clang',
             when='@20180921')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20180921',
             destination='tools',
             placement='clang',
             when='@20180308')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='master',
             destination='projects',
             placement='openmp',
             when='@master')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='release_70',
             destination='projects',
             placement='openmp',
             when='@release_70')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='release_60',
             destination='projects',
             placement='openmp',
             when='@release_60')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20190329',
             destination='projects',
             placement='openmp',
             when='@20190329')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20181226_70',
             destination='projects',
             placement='openmp',
             when='@20181226_70')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20181226_60',
             destination='projects',
             placement='openmp',
             when='@20181226_60')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20180921',
             destination='projects',
             placement='openmp',
             when='@20180921')

    def cmake_args(self):
        spec = self.spec
        # universal
        args = [
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_EH:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
        ]
        args.append('-DPYTHON_EXECUTABLE={0}'.format(
            spec['python'].command.path))

        # needed by flang-driver
        args.append('-DFLANG_LLVM_EXTENSIONS=ON')

        if '+all_targets' not in spec:  # all is default in cmake
            if spec.target.family == 'x86' or spec.target.family == 'x86_64':
                target = 'X86'
            elif spec.target.family == 'arm':
                target = 'ARM'
            elif spec.target.family == 'aarch64':
                target = 'AArch64'
            elif (spec.target.family == 'ppc64' or
                  spec.target.family == 'ppc64le' or
                  spec.target.family == 'ppc' or
                  spec.target.family == 'ppcle'):
                target = 'PowerPC'
            else:
                raise InstallError(
                    'Unsupported architecture: ' + spec.target.family)

            if '+cuda' in spec:
                args.append(
                    '-DLLVM_TARGETS_TO_BUILD:STRING=NVPTX;' + target)
            else:
                args.append(
                    '-DLLVM_TARGETS_TO_BUILD:STRING=' + target)

        # used by openmp
        args.append('-DLIBOMP_USE_HWLOC=On')
        args.append('-DLIBOMP_FORTRAN_MODULES=ON')
        args.append('-DLIBOMP_ENABLE_SHARED=TRUE')

        # used by libomptarget for NVidia gpu
        if '+cuda' in spec:
            args.append('-DOPENMP_ENABLE_LIBOMPTARGET=ON')
            cuda_arch_list = spec.variants['cuda_arch'].value
            args.append('-DCUDA_TOOLKIT_ROOT_DIR=%s' % spec['cuda'].prefix)
            args.append('-DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES={0}'.format(
                ','.join(cuda_arch_list)))
            args.append('-DCLANG_OPENMP_NVPTX_DEFAULT_ARCH=sm_{0}'.format(
                cuda_arch_list[-1]))
        else:
            args.append('-DOPENMP_ENABLE_LIBOMPTARGET=OFF')

        return args

    @run_after("install")
    def post_install(self):
        spec = self.spec

        # Manual bootstrap needed to get NVidia BC compiled with the
        # clang that was just built
        if '+cuda' in spec:
            ompdir = 'build-bootstrapped-omp'
            # rebuild libomptarget to get bytecode runtime library files
            with working_dir(ompdir, create=True):
                args = [
                    self.stage.source_path + '/projects/openmp',
                    '-DCMAKE_C_COMPILER:PATH={0}'.format(
                        spec.prefix.bin + '/clang'),
                    '-DCMAKE_CXX_COMPILER:PATH={0}'.format(
                        spec.prefix.bin + '/clang++'),
                    '-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(
                        spec.prefix)
                ]
                args = args + self.cmake_args()
                # args = self.cmake_args()
                # enable CUDA bitcode
                args.append('-DLIBOMPTARGET_NVPTX_ENABLE_BCLIB=true')
                # work around bad libelf detection in libomptarget
                args.append(
                    '-DCMAKE_CXX_FLAGS:String=-I{0} -I{1}'.format(
                        spec['libelf'].prefix.include,
                        spec['hwloc'].prefix.include))

        cmake(*args)
        make()
        make('install')
