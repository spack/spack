# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Zig(CMakePackage):
    """A general-purpose programming language and toolchain for maintaining
    robust, optimal, and reusable software.
    """

    homepage = "https://ziglang.org/"
    git = "https://github.com/ziglang/zig.git"

    maintainers("alalazo")

    license("MIT")

    version("0.11.0", tag="0.11.0", commit="67709b638224ac03820226c6744d8b6ead59184c")
    version("0.10.1", tag="0.10.1", commit="b57081f039bd3f8f82210e8896e336e3c3a6869b")
    version(
        "0.9.1", tag="0.9.1", commit="6d44a6222d6eba600deb7f16c124bfa30628fb60", deprecated=True
    )

    variant(
        "build_type",
        values=("Release", "RelWithDebInfo", "MinSizeRel"),
        default="Release",
        description="CMake build type",
    )

    depends_on("llvm targets=all")
    depends_on("llvm@13", when="@0.9.1")
    depends_on("llvm@15", when="@0.10.1")
    depends_on("llvm@16", when="@0.11.0")

    depends_on("git", type="build")
    depends_on("ccache")

    provides("ziglang")

    def cmake_args(self):
        return [
            self.define("ZIG_USE_CCACHE", True),
            self.define("ZIG_STATIC_LLVM", True),
            self.define("ZIG_STATIC_ZLIB", True),
        ]
