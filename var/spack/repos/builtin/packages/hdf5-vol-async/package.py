# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5."""

    homepage = "https://hdf5-vol-async.readthedocs.io"
    git      = "https://github.com/hpc-io/vol-async.git"

    maintainers = ['hyoklee', 'houjun', 'jeanbez']

    version('1.0', tag='v1.0')
    version('1.1', tag='v1.1')

    depends_on('mpi')
    depends_on('argobots@main')
    depends_on('hdf5@develop-1.13+mpi+threadsafe')

    def setup_run_environment(self, env):
        env.set('HDF5_PLUGIN_PATH', self.spec.prefix)
        vol_connector = "async"
        env.set('HDF5_VOL_CONNECTOR', vol_connector)
        env.set('MPICH_MAX_THREAD_SAFETY', 'multiple')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        spec = self.spec

        args = [
            self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc),
            self.define('BUILD_SHARED_LIBS:BOOL', True),
            self.define('BUILD_TESTING', self.run_tests)
        ]
        return args

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                make("test")

