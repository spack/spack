# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-async"
    maintainers = ['hyoklee']

    version('v1.0')
    depends_on('argobots@main')
    depends_on('hdf5@1.13.0-rc6+mpi+threadsafe')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBUILD_TESTING:BOOL=ON'
        ]
        return args
