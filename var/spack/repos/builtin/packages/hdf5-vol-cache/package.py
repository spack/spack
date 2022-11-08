# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hdf5VolCache(CMakePackage):
    """Package for HDF5 cache VOL."""

    homepage = "https://vol-cache.readthedocs.io"
    git = "https://github.com/hpc-io/vol-cache.git"

    maintainers = ["hyoklee", "lrknox"]

    version("default", branch="develop")
    version("v1.0", tag="v1.0")

    depends_on("hdf5@1.13:1.13.2 +mpi +threadsafe", when="@:v1.0")
    depends_on("hdf5-vol-async")

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                make("test")
