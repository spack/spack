# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ospray(CMakePackage):
    """Intel OSPRay is an open source, scalable, and portable ray tracing engine for
    high-performance, high-fidelity visualization on Intel Architecture CPUs."""

    homepage = "https://www.ospray.org/"
    url = "https://github.com/ospray/ospray/archive/v2.10.0.tar.gz"
    git = "https://github.com/ospray/ospray.git"

    # maintainers("aumuell")

    version("2.10.0", sha256="bd478284f48d2cb775fc41a2855a9d9f5ea16c861abda0f8dc94e02ea7189cb8")
    version("2.9.0", sha256="0145e09c3618fb8152a32d5f5cff819eb065d90975ee4e35400d2db9eb9f6398")
    version("2.8.0", sha256="2dabc75446a0e2e970952d325f930853a51a9b4d1868c8135f05552a4ae04d39")
    version("2.7.1", sha256="4e7bd8145e19541c04f5d949305f19a894d85a827f567d66ae2eb11a760a5ace")
    version("2.7.0", sha256="bcaeb221b5dd383d27587ffaca7f75d7e0064f64017a0d73df90862b14b5704b")
    version("2.6.0", sha256="5efccd7eff5774b77f8894e68a6b803b535a0d12f32ab49edf13b954e2848f2e")

    variant("apps", default=False, description="Enable building OSPRay Apps")
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
    depends_on("openimagedenoise@1.2.3:")
    depends_on("ispc@1.14.1:", type=("build"))
    depends_on("ispc@1.16.0:", when="@2.7.0:", type=("build"))
    depends_on("ispc@1.18.0:", when="@2.10.0:", type=("build"))
    depends_on("tbb")

    depends_on("mpi", when="+mpi")
    depends_on("snappy@1.1.8:", when="+mpi")

    def cmake_args(self):
        args = [
            self.define("OSPRAY_MODULE_DENOISER", True),
            self.define("OSPRAY_ENABLE_MODULES", True),
            self.define("OSPRAY_ENABLE_APPS", False),
            self.define_from_variant("OSPRAY_MODULE_MPI", "mpi"),
            self.define("OSPRAY_MPI_BUILD_TUTORIALS", False),
            self.define("OSPRAY_ISPC_DIRECTORY", self.spec["ispc"].prefix.bin),
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
