# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cgns(CMakePackage):
    """The CFD General Notation System (CGNS) provides a general, portable,
    and extensible standard for the storage and retrieval of computational
    fluid dynamics (CFD) analysis data."""

    homepage = "http://cgns.github.io/"
    url      = "https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz"
    git      = "https://github.com/CGNS/CGNS"

    version('develop', branch='develop')
    version('master', branch='master')
    version('3.3.1', '65c55998270c3e125e28ec5c3742e15d')
    version('3.3.0', '64e5e8d97144c1462bee9ea6b2a81d7f')

    variant('hdf5', default=True, description='Enable HDF5 interface')
    variant('fortran', default=False, description='Enable Fortran interface')
    variant('scoping', default=True, description='Enable scoping')
    variant('mpi', default=True, description='Enable parallel cgns')
    variant('int64', default=False, description='Build with 64-bit integers')    

    depends_on('hdf5', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCGNS_ENABLE_FORTRAN:BOOL=%s' % (
                'ON' if '+fortran' in spec else 'OFF'),
            '-DCGNS_ENABLE_SCOPING:BOOL=%s' % (
                'ON' if '+scoping' in spec else 'OFF'),
            '-DCGNS_ENABLE_PARALLEL:BOOL=%s' % (
                'ON' if '+mpi' in spec else 'OFF'),
            '-DCGNS_ENABLE_TESTS:BOOL=OFF',
            '-DCGNS_BUILD_CGNSTOOLS:BOOL=OFF'
        ])

        if '+mpi' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
            ])

        options.append(
            '-DCGNS_ENABLE_64BIT:BOOL={0}'.format(
                'ON' if '+int64' in spec else 'OFF'))

        if '+hdf5' in spec:
            options.extend([
                '-DCGNS_ENABLE_HDF5:BOOL=ON',
                '-DHDF5_NEED_ZLIB:BOOL=ON',
                '-DHDF5_INCLUDE_DIR:PATH=%s' % spec['hdf5'].prefix.include,
                '-DHDF5_LIBRARY_DIR:PATH=%s' % spec['hdf5'].prefix.lib
            ])
            if '+mpi' in spec:
                options.extend([
                    '-DHDF5_NEED_MPI:BOOL=ON',
                    '-DHDF5_ENABLE_PARALLEL:BOOL=ON'
                ])
        else:
            options.extend(['-DCGNS_ENABLE_HDF5=OFF'])

        return options
