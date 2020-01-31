# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenpmdApi(CMakePackage):
    """API for easy reading and writing of openPMD files"""

    homepage = "http://www.openPMD.org"
    git      = "https://github.com/openPMD/openPMD-api.git"

    maintainers = ['ax3l']

    version('develop', branch='dev')

    variant('shared', default=True,
            description='Build a shared version of the library')
    variant('mpi', default=True,
            description='Enable parallel I/O')
    variant('hdf5', default=True,
            description='Enable HDF5 support')
    variant('adios1', default=False,
            description='Enable ADIOS1 support')
    variant('adios2', default=False,
            description='Enable ADIOS2 support')
    variant('json', default=True,
            description='Enable JSON support')
    variant('python', default=False,
            description='Enable Python bindings')

    depends_on('cmake@3.11.0:', type='build')
    depends_on('mpark-variant@1.4.0:')
    depends_on('catch@2.6.1: ~single_header', type='test')
    depends_on('mpi@2.3:', when='+mpi')  # might become MPI 3.0+
    depends_on('hdf5@1.8.13:', when='+hdf5')
    depends_on('hdf5@1.8.13: ~mpi', when='~mpi +hdf5')
    depends_on('hdf5@1.8.13: +mpi', when='+mpi +hdf5')
    depends_on('adios@1.13.1:', when='+adios1')
    depends_on('adios@1.13.1: ~mpi', when='~mpi +adios1')
    depends_on('adios@1.13.1: +mpi', when='+mpi +adios1')
    depends_on('adios2@2.4.0:', when='+adios2')
    depends_on('adios2@2.4.0: ~mpi', when='~mpi +adios2')
    depends_on('adios2@2.4.0: +mpi', when='+mpi +adios2')
    depends_on('nlohmann-json@3.7.0:', when='+json')
    depends_on('py-pybind11@2.3.0:', when='+python', type='link')
    depends_on('py-numpy@1.15.1:', when='+python', type=['test', 'run'])
    depends_on('py-mpi4py@2.1.0:', when='+python +mpi', type=['test', 'run'])
    depends_on('python@3.5:', when='+python', type=['link', 'test', 'run'])

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            # variants
            '-DopenPMD_USE_MPI:BOOL={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DopenPMD_USE_HDF5:BOOL={0}'.format(
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DopenPMD_USE_ADIOS1:BOOL={0}'.format(
                'ON' if '+adios1' in spec else 'OFF'),
            '-DopenPMD_USE_ADIOS2:BOOL={0}'.format(
                'ON' if '+adios2' in spec else 'OFF'),
            '-DopenPMD_USE_JSON:BOOL={0}'.format(
                'ON' if '+json' in spec else 'OFF'),
            '-DopenPMD_USE_PYTHON:BOOL={0}'.format(
                'ON' if '+python' in spec else 'OFF'),
            # tests and examples
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBUILD_EXAMPLES:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
        ]

        # switch internally shipped third-party libraries for spack
        if spec.satisfies('+python'):
            args.append('-DopenPMD_USE_INTERNAL_PYBIND11:BOOL=OFF')
            args.append('-DPYTHON_EXECUTABLE:FILEPATH={0}'.format(
                        self.spec['python'].command.path))

        if spec.satisfies('+json'):
            args.append('-DopenPMD_USE_INTERNAL_JSON:BOOL=OFF')

        args.append('-DopenPMD_USE_INTERNAL_VARIANT:BOOL=OFF')
        if self.run_tests:
            args.append('-DopenPMD_USE_INTERNAL_CATCH:BOOL=OFF')

        return args

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        # pre-load dependent CMake-PUBLIC header-only libs
        run_env.prepend_path('CMAKE_PREFIX_PATH', spec['mpark-variant'].prefix)
        run_env.prepend_path('CPATH', spec['mpark-variant'].prefix.include)

        # more deps searched in openPMDConfig.cmake
        if spec.satisfies("+mpi"):
            run_env.prepend_path('CMAKE_PREFIX_PATH', spec['mpi'].prefix)
        if spec.satisfies("+adios1"):
            run_env.prepend_path('CMAKE_PREFIX_PATH', spec['adios'].prefix)
        if spec.satisfies("+adios2"):
            run_env.prepend_path('CMAKE_PREFIX_PATH', spec['adios2'].prefix)
        if spec.satisfies("+hdf5"):
            run_env.prepend_path('CMAKE_PREFIX_PATH', spec['hdf5'].prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # pre-load dependent CMake-PUBLIC header-only libs
        spack_env.prepend_path('CMAKE_PREFIX_PATH',
                               self.spec['mpark-variant'].prefix)
        spack_env.prepend_path('CPATH',
                               self.spec['mpark-variant'].prefix.include)
