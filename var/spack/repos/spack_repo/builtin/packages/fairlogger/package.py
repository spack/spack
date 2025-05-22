# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Fairlogger(CMakePackage):
    """Lightweight and fast C++ Logging Library"""

    homepage = "https://github.com/FairRootGroup/FairLogger"
    url = "https://github.com/FairRootGroup/FairLogger/archive/v1.2.0.tar.gz"
    git = "https://github.com/FairRootGroup/FairLogger.git"
    maintainers("dennisklein", "ChristianTackeGSI")

    version("develop", branch="dev", get_full_repo=True)
    version("2.2.0", sha256="8dfb11e3aa0a9c545f3dfb310d261956727cea558d4123fd8c9c98e135e4d02b")
    version(
        "1.11.1",
        sha256="bba5814f101d705792499e43b387190d8b8c7592466171ae045d4926485f2f70",
        deprecated=True,
    )
    version(
        "1.10.4",
        sha256="2fa321893f2c8c599cca160db243299ce1e941fbfb3f935b1139caa943bc0dba",
        deprecated=True,
    )
    version(
        "1.9.3",
        sha256="0c02076ed708372d5ae7bdebcefc8e45a8cbfa480eea781308336d60a2781f3a",
        deprecated=True,
    )

    generator("make", "ninja", default="ninja")

    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo"),
        multi=False,
        description="CMake build type",
    )
    variant(
        "cxxstd",
        default="default",
        values=(
            "default",
            conditional("11", when="@:1.9"),
            conditional("14", when="@:1"),
            "17",
            "20",
            "23",
            "26",
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant(
        "pretty", default=False, description="Use BOOST_PRETTY_FUNCTION macro (Supported by 1.4+)."
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.9.4:", type="build")
    depends_on("git", type="build", when="@develop")

    depends_on("boost", when="+pretty")
    conflicts("^boost@1.70:", when="^cmake@:3.14")
    depends_on("fmt")
    depends_on("fmt@:8", when="@:1.9")

    def patch(self):
        """FairLogger gets its version number from git.

        The tarball doesn't have that information, so we patch the spack
        version into CMakeLists.txt.
        """
        if not self.spec.satisfies("@develop"):
            filter_file(
                r"(get_git_version\(.*)\)",
                rf"\1 DEFAULT_VERSION {self.spec.version})",
                "CMakeLists.txt",
            )

        if self.spec.satisfies("@:1"):
            filter_file(r"(LANGUAGES C CXX)", r"LANGUAGES CXX", "CMakeLists.txt")

    def cmake_args(self):
        args = [
            self.define("DISABLE_COLOR", True),
            self.define_from_variant("USE_BOOST_PRETTY_FUNCTION", "pretty"),
            self.define("USE_EXTERNAL_FMT", True),
        ]
        if self.spec.variants["cxxstd"].value != "default":
            args.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        if self.spec.satisfies("^boost@:1.69"):
            args.append(self.define("Boost_NO_BOOST_CMAKE", True))
        return args
