# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class AoclSparse(CMakePackage):
    """AOCL-Sparse is a library that contains basic linear algebra subroutines
    for sparse matrices and vectors optimized for AMD EPYC family of processors.
    It is designed to be used with C and C++. Current functionality of sparse
    library supports SPMV function with CSR and ELLPACK formats.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-Sparse license agreement.
    You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/sparse/sparse-libraries-4-0-eula.html
    https://www.amd.com/en/developer/aocl/sparse/sparse-libraries-eula.html
    """

    _name = "aocl-sparse"
    homepage = "https://developer.amd.com/amd-aocl/aocl-sparse/"
    url = "https://github.com/amd/aocl-sparse/archive/3.0.tar.gz"
    git = "https://github.com/amd/aocl-sparse.git"

    maintainers("amd-toolchain-support")

    version("4.0", sha256="68524e441fdc7bb923333b98151005bed39154d9f4b5e8310b5c37de1d69c2c3")
    version("3.2", sha256="db7d681a8697d6ef49acf3e97e8bec35b048ce0ad74549c3b738bbdff496618f")
    version("3.1", sha256="8536f06095c95074d4297a3d2910654085dd91bce82e116c10368a9f87e9c7b9")
    version("3.0", sha256="1d04ba16e04c065051af916b1ed9afce50296edfa9b1513211a7378e1d6b952e")
    version("2.2", sha256="33c2ed6622cda61d2613ee63ff12c116a6cd209c62e54307b8fde986cd65f664")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )
    variant("shared", default=True, description="Build shared library")
    variant("ilp64", default=False, description="Build with ILP64 support")
    variant("examples", default=False, description="Build sparse examples")
    variant("unit_tests", default=False, description="Build sparse unit tests")
    variant("benchmarks", default=False, description="Build Build benchmarks")
    variant(
        "avx",
        default=False,
        when="@4.0: target=zen4:",
        description="Enable experimental AVX512 support",
    )

    depends_on("boost", when="+benchmarks")
    depends_on("boost", when="@2.2")
    depends_on("cmake@3.5:", type="build")

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        build_directory = self.stage.source_path

        if self.spec.variants["build_type"].value == "Debug":
            build_directory = join_path(build_directory, "build", "debug")
        else:
            build_directory = join_path(build_directory, "build", "release")

        return build_directory

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec

        args = [
            "../..",
            "-DCMAKE_INSTALL_PREFIX:PATH={0}".format(spec.prefix),
            "-DCMAKE_CXX_COMPILER={0}".format(os.path.basename(spack_cxx)),
        ]

        if spec.variants["build_type"].value == "Debug":
            args.append("-DCMAKE_BUILD_TYPE=Debug")
        else:
            args.append("-DCMAKE_BUILD_TYPE=Release")

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_CLIENTS_SAMPLES", "examples"))
        args.append(self.define_from_variant("BUILD_CLIENTS_TESTS", "unit_tests"))
        args.append(self.define_from_variant("BUILD_CLIENTS_BENCHMARKS", "benchmarks"))
        args.append(self.define_from_variant("USE_AVX512", "avx"))

        if spec.satisfies("@3.0:"):
            args.append(self.define_from_variant("BUILD_ILP64", "ilp64"))

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        """Simple test to test the built library by running
        one of the aocl-sparse examples, after compiling the
        library with benchmarks.
        """
        dso_suffix = "so" if "+shared" in self.spec else "a"

        if self.spec.variants["build_type"].value == "Debug":
            lib_path = join_path(
                self.build_directory, "library", "libaoclsparse-d.{0}".format(dso_suffix)
            )
        else:
            lib_path = join_path(
                self.build_directory, "library", "libaoclsparse.{0}".format(dso_suffix)
            )

        test_bench_bin = join_path(self.build_directory, "tests", "staging", "aoclsparse-bench")
        test_args = " --function=csrmv --precision=d "
        test_args += "--sizem=1000 --sizen=1000 --sizennz=4000 --verify=1 "
        os.system(test_bench_bin + test_args + lib_path)
