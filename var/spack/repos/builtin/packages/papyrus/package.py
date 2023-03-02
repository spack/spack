# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Papyrus(CMakePackage):
    """Parallel Aggregate Persistent Storage"""

    homepage = "https://code.ornl.gov/eck/papyrus"
    url = "https://code.ornl.gov/eck/papyrus/repository/archive.tar.bz2?ref=v1.0.2"
    git = "https://code.ornl.gov/eck/papyrus.git"

    tags = ["e4s"]

    version("master", branch="master")
    version("1.0.2", sha256="b6cfcff99f73ded8e4ca4b165bc182cd5cac60f0c0cf4f93649b77d074445645")
    version("1.0.1", sha256="3772fd6f2c301faf78f18c5e4dc3dbac57eb361861b091579609b3fff9e0bb17")
    version("1.0.0", sha256="5d57c0bcc80de48951e42460785783b882087a5714195599d773a6eabde5c4c4")

    depends_on("mpi")

    test_requires_compiler = True

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.prepend_path("CPATH", self.prefix.include)
        env.prepend_path("LIBRARY_PATH", lib_dir)
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(join_path("kv", "tests"))

    def test_example(self):
        """Run all c & c++ stand alone test"""

        example_dir = self.test_suite.current_test_cache_dir.kv.tests
        if not os.path.exists(example_dir):
            raise SkipTest("Example directory is missing")

        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        example_list = [
            "01_open_close",
            "02_put_get",
            "03_barrier",
            "04_delete",
            "05_fence",
            "06_signal",
            "07_consistency",
            "08_protect",
            "09_cache",
            "10_checkpoint",
            "11_restart",
            "12_free",
        ]

        mpicxx = which(self.spec["mpi"].mpicxx)
        mpirun = which(self.spec["mpi"].prefix.bin.mpirun)

        for example in example_list:
            test_dir = join_path(example_dir, example)
            if not os.path.exists(test_dir):
                raise SkipTest("{0} is missing".format(test_dir))

            with test_part(
                self,
                f"test_example_{example}",
                purpose=f"build and run {example}",
                work_dir=test_dir,
            ):
                test_example = f"test{example}.c"

                mpicxx(
                    f"{join_path(test_dir, test_example)}",
                    f"-I{self.prefix.include}",
                    f"-L{lib_dir}",
                    "-lpapyruskv",
                    "-g",
                    "-o",
                    example,
                    "-lpthread",
                    "-lm",
                )

                mpirun("-np", "4", example)
