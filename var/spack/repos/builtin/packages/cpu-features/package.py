# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CpuFeatures(CMakePackage):
    """A cross platform C99 library to get cpu features at runtime."""

    homepage = "https://github.com/google/cpu_features"
    git = "https://github.com/google/cpu_features.git"

    version("main", branch="main")
    version("develop", branch="main", deprecated=True)

    version("0.7.0", tag="v0.7.0")
    
    variant("shared", description="Build shared libraries", default=False)

    depends_on("cmake@3.0.0:", type="build")

    def cmake_args(self):
        args = ["-DBUILD_TESTING:BOOL=OFF"]
        args += self.enable_or_disable("BUILD_SHARED_LIBS", variant="shared")
        return args
