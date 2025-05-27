# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class Viskores(CMakePackage, CudaPackage, ROCmPackage):
    """Viskores is a toolkit of scientific visualization algorithms for emerging
    processor architectures. Viskores supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://github.com/Viskores/viskores"
    maintainers("kmorel", "vicentebolea")

    url = "https://github.com/Viskores/Viskores/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/Viskores/Viskores.git"
    tags = ["e4s"]

    test_requires_compiler = True

    version("master", branch="master")
    version("release", branch="release")
    version(
        "1.0.0",
        sha256="5bff5bbd747b7662bb4630889960371d06fcc5e5a962d974a898d1883f196eba",
        preferred=True,
    )

    variant("shared", default=True, description="build shared libs")
    variant("doubleprecision", default=True, description="enable double precision")
    variant("logging", default=True, description="build logging support")
    variant("mpi", default=True, description="build mpi support")
    variant("rendering", default=True, description="build rendering support")
    variant("64bitids", default=False, description="enable 64 bits ids")
    variant("testlib", default=False, description="build test library")
    variant("fpic", default=False, description="build fpic support")
    variant("examples", default=False, description="Install builtin examples")

    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    variant("kokkos", default=False, description="build using Kokkos backend")
    variant(
        "cuda_native", default=True, description="build using native cuda backend", when="+cuda"
    )
    variant("openmp", default=(sys.platform != "darwin"), description="build openmp support")
    variant("tbb", default=(sys.platform == "darwin"), description="build TBB support")
    variant("sycl", default=False, description="Build with SYCL backend")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.12:", type="build")  # CMake >= 3.12
    depends_on("cmake@3.18:", when="+rocm", type="build")  # CMake >= 3.18

    conflicts("%gcc@:4.10", msg="viskores requires gcc >= 5. Please install a newer version")

    depends_on("cuda@10.1.0:", when="+cuda_native")
    depends_on("tbb", when="+tbb")
    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    # Viskores uses the default Kokkos backend
    depends_on("kokkos", when="+kokkos")
    # Viskores native CUDA and Kokkos CUDA backends are not compatible
    depends_on("kokkos ~cuda", when="+kokkos +cuda +cuda_native")
    depends_on("kokkos +cuda", when="+kokkos +cuda ~cuda_native")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda ~cuda_native cuda_arch=%s" % cuda_arch,
        )
    # Viskores uses the Kokkos HIP backend.
    # If Kokkos provides multiple backends, the HIP backend may or
    # may not be used for Viskores depending on the default selected by Kokkos
    depends_on("kokkos +rocm", when="+kokkos +rocm")
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )

    depends_on("hip@3.7:", when="+rocm")
    # CUDA thrust is already include in the CUDA pkg
    depends_on("rocthrust", when="+kokkos+rocm ^cmake@3.24:")

    # It would be better if this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked, not overwritten.
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="~kokkos", msg="Viskores does not support HIP without Kokkos")

    # Viskores uses the Kokkos SYCL backend.
    # If Kokkos provides multiple backends, the SYCL backend may or
    # may not be used for Viskores depending on the default selected by Kokkos
    depends_on("kokkos +sycl", when="+kokkos +sycl")
    conflicts("+sycl", when="~kokkos", msg="Viskores does not support SYCL without Kokkos")
    conflicts("+cuda~cuda_native~kokkos", msg="Cannot have +cuda without a cuda device")
    conflicts("+cuda", when="cuda_arch=none", msg="viskores +cuda requires that cuda_arch be set")

    def cmake_args(self):
        spec = self.spec
        options = []
        gpu_name_table = {
            "30": "kepler",
            "32": "kepler",
            "35": "kepler",
            "50": "maxwell",
            "52": "maxwell",
            "53": "maxwell",
            "60": "pascal",
            "61": "pascal",
            "62": "pascal",
            "70": "volta",
            "72": "turing",
            "75": "turing",
            "80": "ampere",
            "86": "ampere",
        }
        with working_dir("spack-build", create=True):
            is_release = spec.variants["build_type"].value == "Release"
            options = [
                self.define("Viskores_ENABLE_TESTING", False),
                self.define("Viskores_NO_ASSERT", is_release),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("Viskores_ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("Viskores_ENABLE_LOGGING", "logging"),
                self.define_from_variant("Viskores_ENABLE_MPI", "mpi"),
                self.define_from_variant("Viskores_ENABLE_OPENMP", "openmp"),
                self.define_from_variant("Viskores_ENABLE_RENDERING", "rendering"),
                self.define_from_variant("Viskores_ENABLE_TBB", "tbb"),
                self.define_from_variant("Viskores_ENABLE_TESTING_LIBRARY", "testlib"),
                self.define_from_variant("Viskores_INSTALL_EXAMPLES", "examples"),
                self.define_from_variant("Viskores_USE_64BIT_IDS", "64bitids"),
                self.define_from_variant("Viskores_USE_DOUBLE_PRECISION", "doubleprecision"),
                self.define(
                    "Viskores_USE_DEFAULT_TYPES_FOR_ASCENT", "~64bitids +doubleprecision" in spec
                ),
            ]

            if "+tbb" in spec:
                # viskores detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix

            if "+kokkos" in spec and "+rocm" in spec and spec.satisfies("^kokkos@4:"):
                options.append(f"-DCMAKE_CXX_COMPILER:FILEPATH={spec['hip'].prefix.bin.hipcc}")

            # Support for relocatable code
            if "~shared" in spec and "+fpic" in spec:
                options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON")

            # cuda support
            if "+cuda_native" in spec:
                options.append("-DViskores_ENABLE_CUDA:BOOL=ON")
                options.append("-DCMAKE_CUDA_HOST_COMPILER={0}".format(env["SPACK_CXX"]))

                if spec.satisfies("^cmake@3.18:"):
                    options.append(CMakeBuilder.define_cuda_architectures(self))

                else:
                    # Viskores_CUDA_Architecture only accepts a single CUDA arch
                    num_cuda_arch = spec.variants["cuda_arch"].value[0]
                    str_cuda_arch = str()

                    try:
                        str_cuda_arch = gpu_name_table[num_cuda_arch]
                    except KeyError:
                        raise InstallError(f"cuda_arch={num_cuda_arch} needs cmake>=3.18")
                    options.append(f"-DViskores_CUDA_Architecture={str_cuda_arch}")

            else:
                options.append("-DViskores_ENABLE_CUDA:BOOL=OFF")

            # hip support
            if "+rocm" in spec:
                options.append(CMakeBuilder.define_hip_architectures(self))

        return options

    def test_smoke_test(self):
        """Build and run ctests"""
        if "+examples" not in self.spec:
            raise SkipTest("Package must be installed with +examples")

        testdir = "smoke_test_build"
        with working_dir(testdir, create=True):
            cmake = Executable(self.spec["cmake"].prefix.bin.cmake)
            ctest = Executable(self.spec["cmake"].prefix.bin.ctest)

            mpi_home = str()
            if "+mpi" in self.spec:
                mpi_home = self.spec["mpi"].prefix
            cmake(
                self.prefix.share.doc.Viskores.examples.smoke_test,
                f"-DCMAKE_C_COMPILER={self.compiler.cc}",
                f"-DCMAKE_CXX_COMPILER={self.compiler.cxx}",
                f"-DMPI_HOME={mpi_home}",
                f"-DViskores_ROOT={self.prefix}",
            )
            cmake("--build", ".")
            ctest("--verbose")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        self.test_smoke_test()
