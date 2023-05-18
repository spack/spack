# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bricks(CMakePackage):

    """Bricks is a data layout and code generation framework,
    enabling performance-portable stencil computations across
    a multitude of architectures."""

    # url for your package's homepage here.
    homepage = "https://bricks.run/"
    git = "https://github.com/CtopCsUtahEdu/bricklib.git"

    test_requires_compiler = True

    # List of GitHub accounts to notify when the package is updated.
    maintainers("ztuowen", "drhansj")

    version("r0.1", branch="r0.1")

    variant("cuda", default=False, description="Build bricks with CUDA enabled")

    # Building a variant of cmake without openssl is to match how the
    # ECP E4S project builds cmake in their e4s-base-cuda Docker image
    depends_on("cmake", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("opencl-clhpp", when="+cuda")
    depends_on("cuda", when="+cuda")
    depends_on("mpi")

    def cmake_args(self):
        """CMake arguments for configure stage"""
        args = []

        return args

    def flag_handler(self, name, flags):
        """Set build flags as needed"""
        if name in ["cflags", "cxxflags", "cppflags"]:
            # There are many vector instrinsics used in this package. If
            # the package is built on a native architecture, then it likely
            # will not run (illegal instruction fault) on a less feature-
            # rich architecture.
            # If you intend to use this package in an architecturally-
            # heterogeneous environment, then the package should be build
            # with "target=x86_64". This will ensure that all Intel
            # architectures can use the libraries and tests in this
            # project by forceing the AVX2 flag in gcc.
            if name == "cxxflags" and self.spec.target == "x86_64":
                flags.append("-mavx2")
            return (None, flags, None)
        return (flags, None, None)

    @run_after("install")
    def copy_test_sources(self):
        """Files to copy into test cache"""
        srcs = [
            join_path("examples", "external", "CMakeLists.txt"),
            join_path("examples", "external", "main.cpp"),
            join_path("examples", "external", "7pt.py"),
        ]
        self.cache_extra_test_sources(srcs)

    def test(self):
        """Test bricklib package"""
        # Test prebuilt binary
        source_dir = join_path(self.test_suite.current_test_cache_dir, "examples", "external")

        self.run_test(
            exe="cmake", options=["."], purpose="Configure bricklib example", work_dir=source_dir
        )

        self.run_test(
            exe="cmake",
            options=["--build", "."],
            purpose="Build bricklib example",
            work_dir=source_dir,
        )

        self.run_test(
            exe=join_path(source_dir, "example"),
            options=[],
            purpose="Execute bricklib example",
            work_dir=source_dir,
        )
