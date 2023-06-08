# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mlpack(CMakePackage):
    """mlpack is an intuitive, fast, and flexible header-only C++ machine
    learning library with bindings to other languages. It is meant to be
    a machine learning analog to LAPACK, and aims to implement a wide
    array of machine learning methods and functions as a "swiss army knife"
    for machine learning researchers."""

    homepage = "https://www.mlpack.org/"
    url = "https://github.com/mlpack/mlpack/archive/refs/tags/4.0.1.tar.gz"

    maintainers("wdconinc")
    version("4.1.0", sha256="e0c760baf15fd0af5601010b7cbc536e469115e9dd45f96712caa3b651b1852a")
    version("4.0.1", sha256="4c746936ed9da9f16744240ed7b9f2815d3abb90c904071a1d1a628a9bbfb3a5")

    # TODO: Go bindings are not supported due to the absence of gonum in spack
    # variant("go", default=False, description="Build Go bindings")
    variant("julia", default=False, description="Build Julia bindings")
    variant("python", default=False, description="Build Ppython bindings")
    variant("r", default=False, description="Build R bindings")
    variant("shared", default=True, description="Build shared libraries")

    # CMakeLists.txt
    depends_on("cmake@3.6:", type="build")
    depends_on("armadillo@9.800:")
    depends_on("ensmallen@2.10.0:")
    depends_on("cereal@1.1.2:")

    # TODO: Go bindings are not supported due to the absence of gonum in spack
    # with when("+go"):
    #    # ref: src/mlpack/bindings/go/CMakeLists.txt
    #    depends_on("go@1.11.0:")
    #    depends_on("gonum")
    with when("+julia"):
        # ref: src/mlpack/bindings/julia/CMakeLists.txt
        depends_on("julia@0.7.0:")
    with when("+python"):
        # ref: src/mlpack/bindings/python/CMakeLists.txt
        depends_on("py-cython@0.24:")
        depends_on("py-numpy")
        depends_on("py-pandas@0.15.0:")
        # ref: src/mlpack/bindings/python/PythonInstall.cmake
        depends_on("py-pip")
    with when("+r"):
        # ref: src/mlpack/bindings/R/CMakeLists.txt
        depends_on("r@4.0:")
        depends_on("r-roxygen2")
        depends_on("r-rcpp@0.12.12:")
        depends_on("r-rcpparmadillo@0.9.800:")
        depends_on("r-rcppensmallen@0.2.10.0:")
        depends_on("r-testthat")
        depends_on("r-pkgbuild")

    def cmake_args(self):
        args = [
            self.define("BUILD_CLI_EXECUTABLES", True),
            self.define_from_variant("BUILD_GO_BINDINGS", "go"),
            self.define_from_variant("BUILD_JULIA_BINDINGS", "julia"),
            self.define_from_variant("BUILD_PYTHON_BINDINGS", "python"),
            self.define_from_variant("BUILD_R_BINDINGS", "r"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTS", self.run_tests),
            self.define("DOWNLOAD_DEPENDENCIES", False),
        ]
        return args
