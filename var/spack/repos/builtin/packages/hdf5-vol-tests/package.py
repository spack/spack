# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VolTests(CMakePackage):
    """This package tests HDF5 Virtual Object Layer (VOL)."""

    homepage = "https://www.hdfgroup.org"
    git      = "https://github.com/HDFGroup/vol-tests"

    maintainers = ['hyoklee']

    version('master', commit='9a147d3')
    variant('vol-async', default=False, description='Enable async VOL')
    variant('vol-cache', default=False, description='Enable cache VOL')
#    variant('vol-external-passthrough', default=False, 
#            description='Enable external pass-through VOL')
#    variant('vol-log', default=False, 
#            description='Enable log-based VOL')
    variant('vol-adios2', default=False, 
            description='Enable ADIOS2 VOL')
#    variant('vol-rest', default=False, 
#            description='Enable REST VOL')

#    variant('async', default=True, description='Enable parallel tests.')
#    variant('parallel', default=True, description='Enable async API tests.')
    variant('part', default=True, 
            description='Enable building the main test executable.')
    depends_on('szip')
    depends_on('hdf5-vol-async', when='+vol-async')
    depends_on('hdf5-vol-cache', when='+vol-cache')
#    depends_on('hdf5@develop-1.13+mpi+threadsafe', when='+parallel')
#    depends_on('hdf5-vol-external-passthrough', 
#               when='+vol-external-passthrough')
#    depends_on('hdf5-vol-log', when='+vol-log')
    depends_on('adios2+shared+hdf5 ^hdf5@1.12.1', when='+vol-adios2')
#    depends_on('hdf5-vol-rest', when='+vol-rest')

    def cmake_args(self):
        args = []
        if '+parallel' in self.spec:
            args.append('-DHDF5_VOL_TEST_ENABLE_PARALLEL:BOOL=ON')
        if '+async' in self.spec:
            args.append('-DHDF5_VOL_TEST_ENABLE_ASYNC:BOOL=ON')
        if '+part' in self.spec:
            args.append('-DHDF5_VOL_TEST_ENABLE_PART:BOOL=ON')
        return args
