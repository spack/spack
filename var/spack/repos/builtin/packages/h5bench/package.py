# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class H5bench(CMakePackage):
    """A benchmark suite for measuring HDF5 performance."""

    homepage = "https://github.com/hpc-io/h5bench"
    git      = "https://github.com/hpc-io/h5bench.git"

    version('master', branch='master')

    depends_on('cmake@3.10:', type='build')
    depends_on('mpi')
    depends_on('hdf5+mpi@1.12.0:1.99.99,develop-1.12:')

    @run_after('install')
    def install_config(self):
        install_tree('h5bench_patterns/sample_config',
                     self.prefix.share.patterns)
        install('metadata_stress/hdf5_iotest.ini',
                self.prefix.share)

    def setup_build_environment(self, env):
        env.set('HDF5_HOME', self.spec['hdf5'].prefix)
