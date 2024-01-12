# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class VtkM(CMakePackage, CudaPackage, ROCmPackage):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    maintainers("kmorel", "vicentebolea")

    url = "https://gitlab.kitware.com/vtk/vtk-m/-/archive/v1.5.1/vtk-m-v1.5.1.tar.gz"
    git = "https://gitlab.kitware.com/vtk/vtk-m.git"
    tags = ["e4s"]

    test_requires_compiler = True

    version("master", branch="master")
    version("release", branch="release")
    version(
        "2.1.0",
        sha256="9cf3522b6dc0675281a1a16839464ebd1cc5f9c08c20eabee1719b3bcfdcf41f",
        preferred=True,
    )
    version("2.0.0", sha256="32643cf3564fa77f8e2a2a5456a574b6b2355bb68918eb62ccde493993ade1a3")
    version("1.9.0", sha256="12355dea1a24ec32767260068037adeb71abb3df2f9f920c92ce483f35ff46e4")
    version("1.8.0", sha256="fcedee6e8f4ac50dde56e8c533d48604dbfb663cea1561542a837e8e80ba8768")
    version("1.7.1", sha256="7ea3e945110b837a8c2ba49b41e45e1a1d8d0029bb472b291f7674871dbbbb63")
    version("1.7.0", sha256="a86667ac22057462fc14495363cfdcc486da125b366cb568ec23c86946439be4")
    version("1.6.0", sha256="14e62d306dd33f82eb9ddb1d5cee987b7a0b91bf08a7a02ca3bce3968c95fd76")
    version("1.5.5", commit="d2d1c854adc8c0518802f153b48afd17646b6252")
    version("1.5.4", commit="bbba2a1967b271cc393abd043716d957bca97972")
    version("1.5.3", commit="a3b8525ef97d94996ae843db0dd4f675c38e8b1e")
    version("1.5.2", commit="c49390f2537c5ba8cf25bd39aa5c212d6eafcf61")
    version("1.5.1", sha256="64c19e66c0d579cfb21bb0df10d649b523b470b0c9a6c2ea5fd979dfeda2c25e")
    version("1.5.0", sha256="b1b13715c7fcc8d17f5c7166ff5b3e9025f6865dc33eb9b06a63471c21349aa8")
    version("1.4.0", sha256="8d83cca7cd5e204d10da151ce4f1846c1f7414c7c1e579173d15c5ea0631555a")
    version("1.3.0", sha256="f88c1b0a1980f695240eeed9bcccfa420cc089e631dc2917c9728a2eb906df2e")
    version("1.2.0", sha256="607272992e05f8398d196f0acdcb4af025a4a96cd4f66614c6341f31d4561763")
    version("1.1.0", sha256="78618c81ca741b1fbba0853cb5d7af12c51973b514c268fc96dfb36b853cdb18")

    variant("shared", default=False, description="build shared libs")

    variant("doubleprecision", default=True, description="enable double precision")
    variant("logging", default=False, when="@1.3:", description="build logging support")
    variant(
        "virtuals",
        default=False,
        description="enable support for deprecated virtual functions",
        when="@:1.9",
    )
    variant("mpi", default=False, when="@1.3:", description="build mpi support")
    variant("rendering", default=True, description="build rendering support")
    variant("64bitids", default=False, description="enable 64 bits ids")
    variant("testlib", default=False, when="@1.7:", description="build test library")
    variant("fpic", default=False, description="build fpic support")
    variant("examples", default=True, when="@1.8:", description="Install builtin examples")

    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    variant("kokkos", default=False, when="@1.6:", description="build using Kokkos backend")
    variant(
        "cuda_native", default=True, description="build using native cuda backend", when="+cuda"
    )
    variant(
        "openmp",
        default=(sys.platform != "darwin"),
        when="@1.3:",
        description="build openmp support",
    )
    variant("tbb", default=(sys.platform == "darwin"), description="build TBB support")

    depends_on("cmake@3.12:", type="build")  # CMake >= 3.12
    depends_on("cmake@3.18:", when="+rocm", type="build")  # CMake >= 3.18

    conflicts("%gcc@:4.10", msg="vtk-m requires gcc >= 5. Please install a newer version")
    conflicts("%gcc@11:", when="@:1.5.2", msg="DIY has a issue building with gcc 11")

    depends_on("cuda@10.1.0:", when="+cuda_native")
    depends_on("tbb", when="+tbb")
    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    # VTK-m uses the default Kokkos backend
    depends_on("kokkos", when="+kokkos")
    depends_on("kokkos@3.7:3.9", when="@2.0 +kokkos")
    # VTK-m native CUDA and Kokkos CUDA backends are not compatible
    depends_on("kokkos ~cuda", when="+kokkos +cuda +cuda_native")
    depends_on("kokkos +cuda", when="+kokkos +cuda ~cuda_native")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda ~cuda_native cuda_arch=%s" % cuda_arch,
        )
    # VTK-m uses the Kokkos HIP backend.
    # If Kokkos provides multiple backends, the HIP backend may or
    # may not be used for VTK-m depending on the default selected by Kokkos
    depends_on("kokkos +rocm", when="+kokkos +rocm")
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )

    depends_on("hip@3.7:", when="+rocm")
    # CUDA thrust is already include in the CUDA pkg
    depends_on("rocthrust", when="@2.1: +kokkos+rocm")

    # The rocm variant is only valid options for >= 1.7. It would be better if
    # this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked,
    # not overwritten.
    conflicts("+rocm", when="@:1.6")
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="~kokkos", msg="VTK-m does not support HIP without Kokkos")
    conflicts("+rocm", when="+virtuals", msg="VTK-m does not support virtual functions with ROCm")

    # Can build +shared+cuda after @1.7:
    conflicts("+shared", when="@:1.6 +cuda_native")
    conflicts("+cuda~cuda_native~kokkos", msg="Cannot have +cuda without a cuda device")
    conflicts("+cuda~cuda_native", when="@:1.5", msg="Cannot have +cuda without a cuda device")

    conflicts("+cuda", when="cuda_arch=none", msg="vtk-m +cuda requires that cuda_arch be set")

    # Patch
    patch("diy-include-cstddef.patch", when="@1.5.3:1.8.0")

    # VTK-M PR#2972
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/2972
    patch("vtkm-cuda-swap-conflict-pr2972.patch", when="@1.9 +cuda ^cuda@12:")

    # VTK-M PR#3160
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/3160
    patch("mr3160-rocthrust-fix.patch", when="@2.1:")

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
                self.define("VTKm_ENABLE_TESTING", False),
                self.define("VTKm_NO_ASSERT", is_release),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("VTKm_ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("VTKm_ENABLE_LOGGING", "logging"),
                self.define_from_variant("VTKm_ENABLE_MPI", "mpi"),
                self.define_from_variant("VTKm_ENABLE_OPENMP", "openmp"),
                self.define_from_variant("VTKm_ENABLE_RENDERING", "rendering"),
                self.define_from_variant("VTKm_ENABLE_TBB", "tbb"),
                self.define_from_variant("VTKm_ENABLE_TESTING_LIBRARY", "testlib"),
                self.define_from_variant("VTKm_INSTALL_EXAMPLES", "examples"),
                self.define_from_variant("VTKm_NO_DEPRECATED_VIRTUAL", "virtuals"),
                self.define_from_variant("VTKm_USE_64BIT_IDS", "64bitids"),
                self.define_from_variant("VTKm_USE_DOUBLE_PRECISION", "doubleprecision"),
                self.define(
                    "VTKm_USE_DEFAULT_TYPES_FOR_ASCENT", "~64bitids +doubleprecision" in spec
                ),
            ]

            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix

            # Support for relocatable code
            if "~shared" in spec and "+fpic" in spec:
                options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON")

            # cuda support
            if "+cuda_native" in spec:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=ON")
                options.append("-DCMAKE_CUDA_HOST_COMPILER={0}".format(env["SPACK_CXX"]))

                if spec.satisfies("@1.9.0:") and spec.satisfies("^cmake@3.18:"):
                    options.append(self.builder.define_cuda_architectures(self))

                else:
                    # VTKm_CUDA_Architecture only accepts a single CUDA arch
                    num_cuda_arch = spec.variants["cuda_arch"].value[0]
                    str_cuda_arch = str()

                    try:
                        str_cuda_arch = gpu_name_table[num_cuda_arch]
                    except KeyError:
                        raise InstallError(
                            f"cuda_arch={num_cuda_arch} needs cmake>=3.18 & VTK-m>=1.9.0"
                        )
                    options.append(f"-DVTKm_CUDA_Architecture={str_cuda_arch}")

            else:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=OFF")

            # hip support
            if "+rocm" in spec:
                options.append(self.builder.define_hip_architectures(self))

        return options

    # Delegate in the vtk-m built smoke test
    def smoke_test(self):
        spec = self.spec

        if "+examples" not in spec:
            raise RuntimeError(
                "Examples needed for smoke test missing", "reinstall with `+examples` variant"
            )

        testdir = "smoke_test_build"
        with working_dir(testdir, create=True):
            cmake = Executable(spec["cmake"].prefix.bin.cmake)
            ctest = Executable(spec["cmake"].prefix.bin.ctest)
            cmakeExampleDir = spec["vtk-m"].prefix.share.doc.VTKm.examples.smoke_test

            cmake(*([cmakeExampleDir, "-DVTKm_ROOT=" + spec["vtk-m"].prefix]))
            cmake(*(["--build", "."]))
            ctest(*(["--verbose"]))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        self.smoke_test()

    def test(self):
        self.smoke_test()
