# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class ZlibNg(AutotoolsPackage, CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"
    git = "https://github.com/zlib-ng/zlib-ng.git"

    maintainers("haampie")

    license("Zlib")

    version("2.1.6", sha256="a5d504c0d52e2e2721e7e7d86988dec2e290d723ced2307145dedd06aeb6fef2")
    version("2.1.5", sha256="3f6576971397b379d4205ae5451ff5a68edf6c103b2f03c4188ed7075fbb5f04")
    version("2.1.4", sha256="a0293475e6a44a3f6c045229fe50f69dc0eebc62a42405a51f19d46a5541e77a")
    version(
        "2.1.3",
        sha256="d20e55f89d71991c59f1c5ad1ef944815e5850526c0d9cd8e504eaed5b24491a",
        deprecated=True,
    )
    version(
        "2.1.2",
        sha256="383560d6b00697c04e8878e26c0187b480971a8bce90ffd26a5a7b0f7ecf1a33",
        deprecated=True,
    )
    version("2.0.7", sha256="6c0853bb27738b811f2b4d4af095323c3d5ce36ceed6b50e5f773204fb8f7200")
    version("2.0.0", sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8")

    variant("compat", default=True, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")
    variant("shared", default=True, description="Build shared library")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    conflicts("+shared~pic")

    variant("new_strategies", default=True, description="Enable new deflate strategies")

    provides("zlib-api", when="+compat")

    # Default to autotools, since cmake would result in circular dependencies if it's not
    # reused.
    build_system("autotools", "cmake", default="autotools")

    # rpath shenanigans, see https://github.com/zlib-ng/zlib-ng/pull/1546
    with when("@2.1.3"):
        patch("pr-1546.patch", when="platform=darwin")
        patch("pr-1542.patch")  # fix sse4.2 detection
        patch("pr-1561.patch", when="build_system=autotools")  # drop bash dependency
        patch("pr-1562.patch")  # improve intrinsics detection

    # fix building with NVHPC, see https://github.com/zlib-ng/zlib-ng/pull/1698
    # (@2.1.0:2.1.3 need the same changes but in a different file)
    patch("pr-1698.patch", when="@2.1.4:%nvhpc+opt")

    with when("build_system=cmake"):
        depends_on("cmake@3.5.1:", type="build")
        depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")

    conflicts("%nvhpc@:20", msg="the compiler is too old and too broken")

    @property
    def libs(self):
        name = "libz" if self.spec.satisfies("+compat") else "libz-ng"
        return find_libraries(
            name, root=self.prefix, recursive=True, shared=self.spec.satisfies("+shared")
        )

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("+pic build_system=autotools"):
            flags.append(self.compiler.cc_pic_flag)
        if name == "ldflags" and self.spec.satisfies("%cce@17"):
            flags.append("-Wl,--undefined-version")
        return (flags, None, None)


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    @run_before("configure")
    def pretend_gcc(self):
        # All nice things (PIC flags, symbol versioning) that happen to the compilers that are
        # recognized as gcc (%gcc, %clang, %intel, %oneapi) we want for some other compilers too:
        if self.spec.compiler.name in ["nvhpc"]:
            filter_file(r"^gcc=0$", "gcc=1", join_path(self.configure_directory, "configure"))

    def configure_args(self):
        args = []
        if self.spec.satisfies("+compat"):
            args.append("--zlib-compat")
        if self.spec.satisfies("~opt"):
            args.append("--without-optimizations")
        if self.spec.satisfies("~shared"):
            args.append("--static")
        if self.spec.satisfies("~new_strategies"):
            args.append("--without-new-strategies")
        return args


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define_from_variant("ZLIB_COMPAT", "compat"),
            self.define_from_variant("WITH_OPTIM", "opt"),
            self.define("BUILD_SHARED_LIBS", self.spec.satisfies("+shared")),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("WITH_NEW_STRATEGIES", "new_strategies"),
            self.define("ZLIB_ENABLE_TESTS", self.pkg.run_tests),
        ]
