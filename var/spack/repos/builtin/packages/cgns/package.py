# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from spack import *


class Cgns(CMakePackage):
    """The CFD General Notation System (CGNS) provides a general, portable,
    and extensible standard for the storage and retrieval of computational
    fluid dynamics (CFD) analysis data."""

    homepage = "http://cgns.github.io/"
    url      = "https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz"
    git      = "https://github.com/CGNS/CGNS"

    version('develop', branch='develop')
    version('master',  branch='master')
    version('3.4.0',   sha256='6372196caf25b27d38cf6f056258cb0bdd45757f49d9c59372b6dbbddb1e05da')
    version('3.3.1',   sha256='81093693b2e21a99c5640b82b267a495625b663d7b8125d5f1e9e7aaa1f8d469')
    version('3.3.0',   sha256='8422c67994f8dc6a2f201523a14f6c7d7e16313bdd404c460c16079dbeafc662')

    variant('hdf5',    default=True,  description='Enable HDF5 interface')
    variant('fortran', default=False, description='Enable Fortran interface')
    variant('scoping', default=True,  description='Enable scoping')
    variant('mpi',     default=True,  description='Enable parallel cgns')
    variant('int64',   default=False, description='Build with 64-bit integers')

    depends_on('hdf5~mpi', when='+hdf5~mpi')
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

        if self.version <= Version('3.3.1'):
            if sys.platform == 'darwin':
                options.extend([
                    '-DCMAKE_MACOSX_RPATH:BOOL=ON'
                ])

        return options
