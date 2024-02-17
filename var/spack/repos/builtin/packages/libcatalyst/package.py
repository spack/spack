# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess

import llnl.util.tty as tty

from spack.package import *


class Libcatalyst(CMakePackage):
    """Catalyst is an API specification developed for simulations (and other
    scientific data producers) to analyze and visualize data in situ."""

    homepage = "https://gitlab.kitware.com/paraview/catalyst"
    git = "https://gitlab.kitware.com/paraview/catalyst.git"
    url = "https://gitlab.kitware.com/api/v4/projects/paraview%2Fcatalyst/packages/generic/catalyst/v2.0.0/catalyst-v2.0.0.tar.gz"

    license("BSD-3-Clause")

    maintainers("mathstuf", "ayenpure")
    version("master", branch="master")
    version("2.0.0-rc4", sha256="cb491e4ccd344156cc2494f65b9f38885598c16d12e1016c36e2ee0bc3640863")

    variant("mpi", default=False, description="Enable MPI support")
    variant("conduit", default=False, description="Use external Conduit for Catalyst")

    depends_on("mpi", when="+mpi")
    depends_on("conduit", when="+conduit")
    depends_on("cmake@3.26:", type="build")

    def cmake_args(self):
        """Populate cmake arguments for libcatalyst."""
        args = [
            "-DCATALYST_BUILD_TESTING=OFF",
            self.define_from_variant("CATALYST_USE_MPI", "mpi"),
            self.define_from_variant("CATALYST_WITH_EXTERNAL_CONDUIT", "conduit"),
        ]

        return args

    def setup_run_environment(self, env):
        spec = self.spec
        if spec.satisfies("+conduit"):
            env.prepend_path("CMAKE_PREFIX_PATH", spec["conduit"].prefix)

    @on_package_attributes(run_tests=True)
    @run_after("install")
    def build_test(self):
        testdir = "smoke_test_build"
        cmakeExampleDir = join_path(self.stage.source_path, "examples")
        cmake_args = [
            cmakeExampleDir,
            "-DBUILD_SHARED_LIBS=ON",
            self.define("CMAKE_PREFIX_PATH", self.prefix),
        ]
        cmake = which(self.spec["cmake"].prefix.bin.cmake)

        with working_dir(testdir, create=True):
            cmake(*cmake_args)
            cmake(*(["--build", "."]))
            tty.info("Running Catalyst test")

            res = subprocess.run(["adaptor0/adaptor0_test", "catalyst"])
            assert res.returncode == 0
