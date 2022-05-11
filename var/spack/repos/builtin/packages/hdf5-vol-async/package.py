# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-async"
    maintainers = ['hyoklee']

    version('v1.0')
    depends_on('argobots@main')
    depends_on('hdf5@develop-1.13+mpi+threadsafe')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        args = [
            self.define('BUILD_SHARED_LIBS:BOOL', True),
            self.define('BUILD_TESTING:BOOL=ON', self.run_tests)
        ]
        return args
