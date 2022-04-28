# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Adios2(CMakePackage, CudaPackage):
    """The Adaptable Input Output System version 2,
    developed in the Exascale Computing Program"""

    homepage = "https://csmd.ornl.gov/software/adios2"
    url = "https://github.com/ornladios/ADIOS2/archive/v2.8.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS2.git"

    maintainers = ['ax3l', 'chuckatkins', 'williamfgc']

    tags = ['e4s']

    version('master', branch='master')
    version('2.8.0', sha256='5af3d950e616989133955c2430bd09bcf6bad3a04cf62317b401eaf6e7c2d479',
            preferred=True)
    version('2.7.1', sha256='c8e237fd51f49d8a62a0660db12b72ea5067512aa7970f3fcf80b70e3f87ca3e')
    version('2.7.0', sha256='4b5df1a1f92d7ff380416dec7511cfcfe3dc44da27e486ed63c3e6cffb173924')
    version('2.6.0', sha256='45b41889065f8b840725928db092848b8a8b8d1bfae1b92e72f8868d1c76216c')
    version('2.5.0', sha256='7c8ff3bf5441dd662806df9650c56a669359cb0185ea232ecb3578de7b065329')
    version('2.4.0', sha256='50ecea04b1e41c88835b4b3fd4e7bf0a0a2a3129855c9cc4ba6cf6a1575106e2')
    version('2.3.1', sha256='3bf81ccc20a7f2715935349336a76ba4c8402355e1dc3848fcd6f4c3c5931893')

    # General build options
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # There's not really any consistency about how static and shared libs are
    # implemented across spack.  What we're trying to support is specifically three
    # library build types:
    #   shared (which is implicitly w/ pic)
    #     Implemented by +shared +pic
    #   static w/o pic
    #     Implemented by ~shared ~pic
    #   static w/ pic
    #     Implemented by ~shared +pic
    # shared w/o pic is not a valid configuration because shared libraries are Position
    # Independent # Code by design.  We're not inherently tied to this approach and can
    # change how we're supporting differnt library types in the package at anytime if
    # spack decides on a standardized way of doing it across packages
    variant('shared', default=True, when='+pic', description='Build shared libraries')
    variant('pic', default=True, description='Build pic-enabled static libraries')

    # Features
    variant('mpi', default=True, description='Enable MPI')

    # Compression libraries
    variant('blosc', default=True, when='@2.4:', description='Enable Blosc compression')
    variant('bzip2', default=True, when='@2.4:', description='Enable BZip2 compression')
    variant('zfp', default=True, description='Enable ZFP compression')
    variant('png', default=True, when='@2.4:', description='Enable PNG compression')
    variant('sz', default=True, description='Enable SZ compression')

    # Rransport engines
    variant('sst', default=True, description='Enable the SST staging engine')
    variant('dataman', default=False, when='+shared',
            description='Enable the DataMan engine for WAN transports')
    variant('dataspaces', default=False, when='@2.5:',
            description='Enable support for DATASPACES')
    variant('ssc', default=True, description='Enable the SSC staging engine')
    variant('hdf5', default=False, description='Enable the HDF5 engine')

    # Optional language bindings, C++11 and C always provided
    variant('cuda', default=False, when='@2.8:', description='Enable CUDA support')
    variant('python', default=False, description='Enable the Python bindings')
    variant('fortran', default=True, description='Enable the Fortran bindings')

    # Requires mature C++11 implementations
    conflicts('%gcc@:4.7')
    conflicts('%intel@:15')
    conflicts('%pgi@:14')

    depends_on('cmake@3.12.0:', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libffi', when='+sst')            # optional in DILL
    depends_on('libfabric@1.6.0:', when='+sst')  # optional in EVPath and SST
    # depends_on('bison', when='+sst')     # optional in FFS, broken package
    # depends_on('flex', when='+sst')      # optional in FFS, depends on BISON

    depends_on('mpi', when='+mpi')
    depends_on('libzmq', when='+dataman')
    depends_on('dataspaces@1.8.0:', when='+dataspaces')

    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')

    depends_on('c-blosc', when='+blosc')
    depends_on('bzip2', when='+bzip2')
    depends_on('libpng@1.6:', when='+png')
    depends_on('zfp@0.5.1:', when='+zfp')
    depends_on('sz@2.0.2.0:', when='+sz')

    extends('python', when='+python')
    depends_on('python@2.7:2.8,3.5:', when='@:2.4.0 +python', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@:2.4.0',         type='test')
    depends_on('python@3.5:',         when='@2.5.0: +python', type=('build', 'run'))
    depends_on('python@3.5:',         when='@2.5.0:',         type='test')
    depends_on('py-numpy@1.6.1:',     when='+python',         type=('build', 'run'))
    depends_on('py-mpi4py@2.0.0:',    when='+mpi +python',    type=('build', 'run'))

    # Fix findmpi when called by dependees
    # See https://github.com/ornladios/ADIOS2/pull/1632
    patch('cmake-update-findmpi.patch', when='@2.4.0')

    # Fix the signature of the builtin clear_cache function in the
    # third-party dill library.
    # See https://github.com/ornladios/ADIOS2/pull/1899
    patch('2.5-fix-clear_cache.patch', when='@2.5.0')

    # Fix an unnecessary python dependency when testing is disabled
    # See https://github.com/ornladios/ADIOS2/pull/2596
    patch('2.7-fix-python-test-deps.patch', when='@2.5.0:2.7.0')

    # Fix unresolved symbols when built with gcc10.
    # See https://github.com/ornladios/ADIOS2/pull/2714
    patch('2.6-fix-gcc10-symbols.patch', when='@2.6.0')

    # Add missing include <memory>
    # https://github.com/ornladios/adios2/pull/2710
    patch('https://github.com/ornladios/adios2/pull/2710.patch?full_index=1', when='@:2.7.1',
          sha256='8221073d1b2f8944395a88a5d60a15c7370646b62f5fc6309867bbb6a8c2096c')

    @when('%fj')
    def patch(self):
        """ add fujitsu mpi commands #16864 """
        f = join_path('cmake', 'upstream', 'FindMPI.cmake')
        filter_file('mpcc_r)', 'mpcc_r mpifcc)', f, string=True)
        filter_file('mpc++_r)', 'mpcc_r mpiFCC)', f, string=True)
        filter_file('mpf77_r', 'mpf77_r mpifrt', f, string=True)

    def setup_build_environment(self, env):
        # https://github.com/ornladios/ADIOS2/issues/2228
        if self.spec.satisfies('%gcc@10: +fortran'):
            env.set('FFLAGS', '-fallow-argument-mismatch')
        elif self.spec.satisfies('%fj +fortran'):
            env.set('FFLAGS', '-Ccpp')

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        args = [
            from_variant('CMAKE_POSITION_INDEPENDENT_CODE', 'pic'),
            from_variant('BUILD_SHARED_LIBS', 'shared'),
            from_variant('ADIOS2_USE_Blosc', 'blosc'),
            from_variant('ADIOS2_USE_BZip2', 'bzip2'),
            from_variant('ADIOS2_USE_DataMan', 'dataman'),
            from_variant('ADIOS2_USE_DataSpaces', 'dataspaces'),
            from_variant('ADIOS2_USE_Fortran', 'fortran'),
            from_variant('ADIOS2_USE_HDF5', 'hdf5'),
            from_variant('ADIOS2_USE_MPI', 'mpi'),
            from_variant('ADIOS2_USE_PNG', 'png'),
            from_variant('ADIOS2_USE_Python', 'python'),
            from_variant('ADIOS2_USE_SSC', 'ssc'),
            from_variant('ADIOS2_USE_SST', 'sst'),
            from_variant('ADIOS2_USE_SZ', 'sz'),
            from_variant('ADIOS2_USE_ZFP', 'zfp'),
            from_variant('ADIOS2_USE_CUDA', 'cuda'),
            self.define('BUILD_TESTING', self.run_tests),
            self.define('ADIOS2_BUILD_EXAMPLES', False),
            self.define('ADIOS2_USE_Endian_Reverse', True),
            self.define('ADIOS2_USE_IME', False),
            self.define('ADIOS2_USE_MGARD', False)
        ]

        if '+sst' in spec:
            args.extend([
                # Broken dependency package
                '-DCMAKE_DISABLE_FIND_PACKAGE_BISON=TRUE',
                # Depends on ^
                '-DCMAKE_DISABLE_FIND_PACKAGE_FLEX=TRUE',

                # Not yet packaged
                '-DCMAKE_DISABLE_FIND_PACKAGE_CrayDRC=TRUE',
                '-DCMAKE_DISABLE_FIND_PACKAGE_NVSTREAM=TRUE'
            ])

        if '%fj' in spec:
            args.extend([
                '-DCMAKE_Fortran_SUBMODULE_EXT=.smod',
                '-DCMAKE_Fortran_SUBMODULE_SEP=.'
            ])

        if '+python' in spec or self.run_tests:
            args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s' % spec['python'].command.path)

        return args

    @property
    def libs(self):
        spec = self.spec
        libs_to_seek = set()

        if '@2.6:' in spec:
            libs_to_seek.add('libadios2_core')
            libs_to_seek.add('libadios2_c')
            libs_to_seek.add('libadios2_cxx11')
            if '+fortran' in spec:
                libs_to_seek.add('libadios2_fortran')

            if '+mpi' in spec:
                libs_to_seek.add('libadios2_core_mpi')
                libs_to_seek.add('libadios2_c_mpi')
                libs_to_seek.add('libadios2_cxx11_mpi')
                if '+fortran' in spec:
                    libs_to_seek.add('libadios2_fortran_mpi')

            if '@2.7: +shared+hdf5' in spec and '@1.12:' in spec['hdf5']:
                libs_to_seek.add('libadios2_h5vol')

        else:
            libs_to_seek.add('libadios2')
            if '+fortran' in spec:
                libs_to_seek.add('libadios2_fortran')

        return find_libraries(list(libs_to_seek), root=self.spec.prefix,
                              shared=('+shared' in spec), recursive=True)

    def setup_run_environment(self, env):
        try:
            all_libs = self.libs
            idx = all_libs.basenames.index('libadios2_h5vol.so')
            env.prepend_path('HDF5_PLUGIN_PATH', os.path.dirname(all_libs[idx]))
        except ValueError:
            pass
