# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5.  WARNING: Please refer to the
    documentation.  This package will be available in HDF5_PLUGIN_PATH, but in order to
    use it the consumer must set the HDF5_VOL_CONNECTOR environment variable."""

    homepage = "https://hdf5-vol-async.readthedocs.io"
    git = "https://github.com/hpc-io/vol-async.git"

    maintainers = ["hyoklee", "houjun", "jeanbez"]

    tags = ["e4s"]

    version("develop", branch="develop")
    version("1.3", tag="v1.3")
    version("1.2", tag="v1.2")
    version("1.1", tag="v1.1")
    version("1.0", tag="v1.0")

    depends_on("mpi")
    depends_on("argobots@1.1:")
    depends_on("hdf5@1.13:1.13.2 +mpi +threadsafe", when="@:1.3")

    # Enforce that MPI_THREAD_MULTIPLE is available.
    depends_on("openmpi +thread_multiple", when="^openmpi")
    depends_on("mvapich2 threads=multiple", when="^mvapich2")

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
        env.set("MPICH_MAX_THREAD_SAFETY", "multiple")

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        args = [
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                make("test")
