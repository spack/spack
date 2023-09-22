# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ospray(CMakePackage):
    """Intel OSPRay is an open source, scalable, and portable ray tracing engine for
    high-performance, high-fidelity visualization on Intel Architecture CPUs."""

    homepage = "https://www.ospray.org/"
    git = "https://github.com/BlueBrain/ospray.git"

    version("2.10.1", tag="v2.10.1")
    version("2.10.4", tag="v2.10.4")
    version("2.10.5", tag="v2.10.5")
    version("2.10.6", tag="v2.10.6")

    variant("apps", default=False, description="Enable building OSPRay Apps")
    variant("denoiser", default=False, description="Enable denoiser image operation")
    variant("glm", default=False, description="Build ospray_cpp GLM tests/tutorial")
    variant("mpi", default=True, description="Enable MPI support")

    depends_on("rkcommon@1.5:")
    depends_on("rkcommon@1.7:1.9", when="@2.7.0:2.8")
    depends_on("rkcommon@1.9", when="@2.9.0")
    depends_on("rkcommon@1.10:", when="@2.10.0:")
    depends_on("embree@3.12: +ispc")
    depends_on("embree@3.13.1:", when="@2.7.0:")
    depends_on("openvkl@0.13.0:")
    depends_on("openvkl@1.0.1:", when="@2.7.0:")
    depends_on("openvkl@1.2.0:", when="@2.9.0:")
    depends_on("openvkl@1.3.0:", when="@2.10.0:")
    depends_on("openimagedenoise@1.2.3:", when="+denoiser")
    depends_on("ispc@1.14.1:", type=("build"))
    depends_on("ispc@1.16.0:", when="@2.7.0:", type=("build"))
    depends_on("ispc@1.18.0:", when="@2.10.0:", type=("build"))
    depends_on("tbb")

    depends_on("mpi", when="+mpi")
    depends_on("snappy@1.1.8:", when="+mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("OSPRAY_MODULE_DENOISER", "denoiser"),
            self.define("OSPRAY_ENABLE_MODULES", True),
            self.define("OSPRAY_ENABLE_APPS", False),
            self.define_from_variant("OSPRAY_MODULE_MPI", "mpi"),
            self.define("OSPRAY_MPI_BUILD_TUTORIALS", False),
            self.define("OSPRAY_ISPC_DIRECTORY", self.spec["ispc"].prefix.bin),
            self.define_from_variant("OSPRAY_APPS_ENABLE_GLM", "glm"),
        ]

        # Apps
        enable_apps_arg = "" if self.spec.satisfies("@2.9:") else "ENABLE_"
        args.extend(
            [
                self.define("OSPRAY_{0}APPS_TESTING".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_EXAMPLES".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_TUTORIALS".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_BENCHMARK".format(enable_apps_arg), False),
            ]
        )

        return args
