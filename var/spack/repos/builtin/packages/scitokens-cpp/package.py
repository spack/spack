# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ScitokensCpp(CMakePackage):
    """A C++ implementation of the SciTokens library with a C library interface.
    SciTokens provide a token format for distributed authorization."""

    homepage = "https://github.com/scitokens/scitokens-cpp"
    url = "https://github.com/scitokens/scitokens-cpp/archive/refs/tags/v0.7.0.tar.gz"

    version("0.7.3", sha256="7d3c438596588cd74cf1af8255c55f44ca86a34293b81415ee24b33de64f886a")
    version("0.7.2", sha256="594eee5f80463cd501e9b4c17b6ea6dcae47a42ef4947406ce8b157e15d50d5b")
    version("0.7.1", sha256="44a1bca188897b1e97645149d1f6bc187cd0e482ad36159ca376834f028ce5ef")
    version("0.7.0", sha256="72600cf32523b115ec7abf4ac33fa369e0a655b3d3b390e1f68363e6c4e961b6")

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    depends_on("sqlite")
    depends_on("curl")
    depends_on("jwt-cpp", type="build")
    depends_on("uuid", type="build")

    conflicts("jwt-cpp@0.5:", when="@:0.7")

    # https://github.com/scitokens/scitokens-cpp/issues/72
    @when("^openssl@3:")
    def patch(self):
        filter_file(" -Werror", "", "CMakeLists.txt")

    def cmake_args(self):
        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant
        args = [
            define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            define("CMAKE_CXX_STANDARD_REQUIRED", True)
        ]
        return args

    def setup_build_environment(self, env):
        spec=self.spec
        env.set("JWC_CPP_DIR", spec["jwt-cpp"].prefix)
