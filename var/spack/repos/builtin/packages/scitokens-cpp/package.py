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

    maintainers("gartung", "greenc-FNAL", "marcmengel", "vitodb")

    version("1.0.1", sha256="d4660521fa17189e7a7858747d066052dd8ea8f430ce7649911c157d4423c412")
    version("1.0.0", sha256="88376c5cd065aac8d92445184a02ccf5186dc4890ccd7518e88be436978675c0")
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

    depends_on("cmake@2.6:")
    depends_on("cmake@3.10:", when="@0.7.1:")
    depends_on("openssl")
    depends_on("sqlite")
    depends_on("curl")
    depends_on("jwt-cpp", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("uuid", type="build")

    conflicts("jwt-cpp@0.5:", when="@:0.7")

    # https://github.com/scitokens/scitokens-cpp/issues/72
    @when("@0.7.0 ^openssl@3:")
    def patch(self):
        filter_file(" -Werror", "", "CMakeLists.txt")

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        args = [
            define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            define("CMAKE_CXX_STANDARD_REQUIRED", True),
        ]
        return args

    def setup_build_environment(self, env):
        env.set("JWC_CPP_DIR", self.spec["jwt-cpp"].prefix)
