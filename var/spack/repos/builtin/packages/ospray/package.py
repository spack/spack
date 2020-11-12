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

    variant("apps", default=False, description="Build example applications")

    depends_on("cmake@3.1:", type="build")
    depends_on("ispc@:1.12", type="build", when="@:1.999")
    depends_on("ninja", type="build")
    depends_on("embree")
    depends_on("mpi")
    depends_on("tbb")

    conflicts("^gcc")

    def cmake_args(self):
        return [
            "-DOSPRAY_ENABLE_TUTORIALS=OFF",
            "-DOSPRAY_ENABLE_APPS:BOOL={0}".format(
                "ON" if "+apps" in self.spec else "OFF"
            ),
            "-DOSPRAY_MODULE_MPI=ON",
        ]
