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

    variant('mpi', default=True,
            description='Enable parallel I/O')
    variant('hdf5', default=True,
            description='Enable HDF5 support')
    variant('adios1', default=False,
            description='Enable ADIOS1 support')
    variant('adios2', default=False,
            description='Enable ADIOS2 support')
    # variant('json', default=True,
    #         description='Enable JSON support')
    variant('python', default=True,
            description='Enable Python bindings')

    depends_on('cmake@3.10.0:', type='build')
    depends_on('mpark-variant@1.3.0:')
    depends_on('catch@2.3.0: ~single_header', type='test')
    depends_on('mpi@2.3:', when='+mpi')  # might become MPI 3.0+
    depends_on('hdf5@1.8.13:', when='+hdf5')
    depends_on('hdf5@1.8.13: ~mpi', when='~mpi +hdf5')
    depends_on('hdf5@1.8.13: +mpi', when='+mpi +hdf5')
    depends_on('adios@1.10.0:', when='+adios1')
    depends_on('adios@1.10.0: ~mpi', when='~mpi +adios1')
    depends_on('adios@1.10.0: +mpi', when='+mpi +adios1')
    depends_on('adios2@2.1.0:', when='+adios2')
    depends_on('adios2@2.1.0: ~mpi', when='~mpi +adios2')
    depends_on('adios2@2.1.0: +mpi', when='+mpi +adios2')
    # ideally we want 2.3.0+ for full C++11 CT function signature support
    depends_on('py-pybind11@2.2.3:', when='+python')
    depends_on('py-numpy@1.15.1:', when='+python', type=['test', 'run'])

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec

        args = [
            # variants
            '-DopenPMD_USE_MPI:BOOL={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DopenPMD_USE_HDF5:BOOL={0}'.format(
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DopenPMD_USE_ADIOS1:BOOL={0}'.format(
                'ON' if '+adios1' in spec else 'OFF'),
            '-DopenPMD_USE_ADIOS2:BOOL={0}'.format(
                'ON' if '+adios2' in spec else 'OFF'),
            # '-DopenPMD_USE_JSON:BOOL={0}'.format(
            #     'ON' if '+json' in spec else 'OFF'),
            '-DopenPMD_USE_PYTHON:BOOL={0}'.format(
                'ON' if '+python' in spec else 'OFF'),
            # tests and examples
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBUILD_EXAMPLES:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
        ]

        if spec.satisfies('+python'):
            args.append('-DopenPMD_USE_INTERNAL_PYBIND11:BOOL=OFF')
            args.append('-DPYTHON_EXECUTABLE:FILEPATH={0}'.format(
                        self.spec['python'].command.path))

        # switch internally shipped third-party libraries for spack
        args.append('-DopenPMD_USE_INTERNAL_VARIANT:BOOL=OFF')
        if self.run_tests:
            args.append('-DopenPMD_USE_INTERNAL_CATCH:BOOL=OFF')

        return args
