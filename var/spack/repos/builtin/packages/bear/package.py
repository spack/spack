# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bear(CMakePackage):
    """Bear is a tool that generates a compilation database for clang tooling
    from non-cmake build systems."""

    homepage = "https://github.com/rizsotto/Bear"
    git = "git@github.com:rizsotto/Bear.git"
    url = "https://github.com/rizsotto/Bear/archive/2.0.4.tar.gz"
    maintainers("vmiheer", "trws")

    version("3.0.20", sha256="45cfcdab07f824f6c06c9776701156f7a04b23eadd25ecbc88c188789a447cc7")
    version("3.0.19", sha256="2fcfe2c6e029182cfc54ed26b3505c0ef12b0f43df03fb587f335afdc2ca9431")
    version("3.0.18", sha256="ae94047c79b4f48462b66981f66a67b6a833d75d4c40e7afead491b1865f1142")
    version("3.0.0", sha256="7b68aad69e887d945ad20f8e9f3a8c33cf2d59cc80da7e52d931d8c685fe2f79")
    version("2.2.0", sha256="6bd61a6d64a24a61eab17e7f2950e688820c72635e1cf7ea8ea7bf9482f3b612")
    version("2.0.4", sha256="33ea117b09068aa2cd59c0f0f7535ad82c5ee473133779f1cc20f6f99793a63e")

    depends_on("pkgconfig", when="@3:")
    depends_on("fmt", when="@3.0.0:")
    depends_on("grpc", when="@3.0.0:")
    depends_on("nlohmann-json", when="@3.0.0:")
    depends_on("spdlog", when="@3.0.0:")
    depends_on("cmake@2.8:", type="build")
    depends_on("python", type="build")
    depends_on("googletest", type="test", when="@3:")

    patch("rpath-handling-3.0.20.patch", when="@3.0.20:")

    def cmake_args(self):
        return [
            "-DENABLE_UNIT_TESTS={}".format("ON" if self.run_tests else "OFF"),
            "-DENABLE_FUNC_TESTS=OFF",
            "-DENABLE_MULTILIB=OFF",
        ]
