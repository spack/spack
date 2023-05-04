# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5.

    Usage: Set the HDF5_VOL_CONNECTOR environment variable to enable this adaptor, i.e.

        $export HDF5_VOL_CONNECTOR="async under_vol=0;under_info={}"

    ref. https://hdf5-vol-async.readthedocs.io/en/latest/gettingstarted.html#set-environmental-variables
    """

    homepage = "https://hdf5-vol-async.readthedocs.io"
    git = "https://github.com/hpc-io/vol-async.git"

    maintainers("hyoklee", "houjun", "jeanbez")

    tags = ["e4s"]

    version("develop", branch="develop")
    version("1.5", tag="v1.5")
    version("1.4", tag="v1.4")
    version("1.3", tag="v1.3")
    version("1.2", tag="v1.2")
    version("1.1", tag="v1.1")
    version("1.0", tag="v1.0")

    variant("memcpy", default=False, description="Enable buffer copy for dataset write")

    depends_on("mpi")
    depends_on("argobots@1.1:")
    depends_on("hdf5 +mpi +threadsafe")
    depends_on("hdf5@1.13.0:1.13.2", when="@:1.3")
    depends_on("hdf5@1.13.3:", when="@1.4:")

    # Require MPI_THREAD_MULTIPLE.
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
            self.define_from_variant("ENABLE_WRITE_MEMCPY", "memcpy"),
        ]
        return args

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                make("test")
