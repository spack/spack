# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ospray(CMakePackage):
    """A Ray Tracing Based Rendering Engine for High-Fidelity Visualization"""

    homepage = "https://www.ospray.org/"
    git = "https://github.com/ospray/ospray.git"
    generator = "Ninja"

    version("1.8.5", tag="v1.8.5")
    version("1.7.3", tag="v1.7.3")
    version("2.9.0", tag="v2.9.0")

    variant("apps", default=False, description="Build example applications")

    depends_on("cmake@3.1:", type="build")
    depends_on("ispc@:1.12", type="build", when="@:1.999")
    depends_on("ispc@1.16.1:", type="build", when="@2.9.0:")
    depends_on("ninja", type="build")
    depends_on("embree")
    depends_on("mpi")
    depends_on("tbb")
    depends_on("rkcommon", when="@2.9.0:")
    depends_on("openvkl", when="@2.9.0:")
    depends_on("snappy", when="@2.9.0:")

    conflicts("^gcc")

    def cmake_args(self):
        args = [
            "-DOSPRAY_ENABLE_TUTORIALS=OFF",
            "-DOSPRAY_MODULE_MPI=ON"
        ]
        if self.spec.satisfies('@:1.8.5'):
            args.append("-DOSPRAY_ENABLE_APPS:BOOL={0}".format(
                        "ON" if "+apps" in self.spec else "OFF"))
        elif self.spec.satisfies('@:2.9.0'):
            args.append("-DOSPRAY_MODULE_DENOISER=OFF")
            args.append("-DOSPRAY_ENABLE_APPS_BENCHMARK={0}".format(
                        "ON" if "+apps" in self.spec else "OFF"))
            args.append("-DOSPRAY_ENABLE_APPS_EXAMPLES={0}".format(
                        "ON" if "+apps" in self.spec else "OFF"))
            args.append("-DOSPRAY_ENABLE_APPS_TESTING={0}".format(
                        "ON" if "+apps" in self.spec else "OFF"))
            args.append("-DOSPRAY_ENABLE_APPS_TUTORIALS={0}".format(
                        "ON" if "+apps" in self.spec else "OFF"))
            args.append("-DOSPRAY_APPS_ENABLE_GLM=OFF")

        return args
