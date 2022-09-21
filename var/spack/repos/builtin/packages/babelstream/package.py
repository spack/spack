# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Babelstream(CMakePackage):
    """Measure memory transfer rates to/from global device memory on GPUs.
    This benchmark is similar in spirit, and based on, the STREAM benchmark for CPUs."""

    homepage = "https://github.com/UoB-HPC/BabelStream"
    git = "https://github.com/UoB-HPC/BabelStream.git"
    url = "https://github.com/UoB-HPC/BabelStream/archive/refs/tags/v4.0.tar.gz"

    maintainers = ["robj0nes ", "tomdeakin", "tom91136"]

    version("main", branch="main")
    version("develop", branch="develop")
    version("4.0", sha256="a9cd39277fb15d977d468435eb9b894f79f468233f0131509aa540ffda4f5953")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )

    variant(
        "model",
        values=[
            "std-data",
            "std-indices",
            "std-ranges",
            "ocl",
            "omp",
            "hip",
            "cuda",
            "kokkos",
            "sycl",
            "sycl2020",
            "acc",
            "raja",
            "tbb",
            "thrust",
        ],
        default="std-data",
        description="Specify the model to be built",
    )

    # TODO: Will likely need revising once PR #29761 has been merged. 
    variant("flags", values=str, default=" ", description="Additional CXX flags to be provided")

    variant(
        "amd_arch", values=str, default="none", description="Target AMD GPU device being used."
    )

    variant(
        "cuda_arch", values=str, default="none", description="The CUDA architecture being used."
    )

    variant("cuda", default=False, description="Enable CUDA support")
    variant("opencl", default=False, description="Enable OpenCL support")
    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("cuda", when="+cuda")
    # Note: At time of testing POCL 3.0 has build failure issues.
    depends_on("pocl@1.8", when="+opencl")
    depends_on("pocl@1.8", when="model=ocl")
    depends_on("openmpi", when="+openmp")
    depends_on("openmpi", when="model=omp")

    for variant in ["+cuda", "+openmp"]:
        with when(variant):
            for model in ["kokkos", "raja"]:
                with when("model=" + model):
                    depends_on(model + variant)
    with when("~cuda") and when("~openmp"):
        for model in ["kokkos", "raja"]:
            with when("model=" + model):
                depends_on(model)

    for model in ["sycl", "sycl2020"]:
        with when("model=" + model):
            depends_on("intel-oneapi-compilers", when="model=" + model)

    with when("model=tbb"):
        depends_on("opencv")
        depends_on("intel-oneapi-tbb")

    with when("model=hip"):
        depends_on("hip@5.2.0")
        conflicts(
            "amd_arch=none",
            when="~cuda",
            msg="HIP requires AMD architecture to be specified by amd_arch=",
        )

    conflicts("~cuda", when="model=cuda", msg="CUDA requires +cuda variant")
    conflicts("~cuda", when="model=thrust", msg="Thrust requires +cuda variant")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="CUDA requires architecture to be specfied by cuda_arch=",
    )

    def cmake_args(self):
        args = [
            "-DMODEL=" + self.spec.variants["model"].value,
            "-DRELEASE_FLAGS=",
            "-DCXX_EXTRA_FLAGS=" + self.spec.variants["flags"].value + " -O3",
        ]

        model = self.spec.variants["model"].value

        if model not in ["kokkos", "raja", "acc", "hip"]:
            args.append("-DCMAKE_CXX_COMPILER_FORCED=True")

        if self.spec.satisfies("+cuda"):
            args.append("-DCUDA_ARCH=" + self.spec.variants["cuda_arch"].value)
            cuda_comp = self.spec["cuda"].prefix + "/bin/nvcc"
            args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
            # TODO: RAJA CUDA builds not working
            if "raja" in model:
                cuda_dir = self.spec["cuda"].prefix
                for flag in [
                    "-DENABLE_CUDA=ON",
                    "-DTARGET=NVIDIA",
                    "-DCUDA_TOOLKIT_ROOT_DIR=" + cuda_dir,
                    "-DCMAKE_CUDA_ARCHITECTURES=80",
                ]:
                    args.append(flag)

        if self.spec.satisfies("+opencl") or "ocl" in model:
            ocl_lib = self.spec["pocl"].prefix + "/lib64/libOpenCL.so"
            args.append("-DOpenCL_LIBRARY=" + ocl_lib)

        if "std-ranges" in model:
            args.append(
                "-DCXX_EXTRA_FLAGS= --std=c++2a " + self.spec.variants["flags"].value + " -O3"
            )

        if "acc" in model:
            for flag in [
                "-DCMAKE_CXX_COMPILER=" + self.compiler.cxx,
                "-DTARGET_DEVICE=gpu",
                "-DOpenACC_CXX_FLAGS= ",
            ]:
                args.append(flag)

        if "hip" in model:
            hip_comp = self.spec["hip"].prefix + "/bin/hipcc"
            args.append("-DCMAKE_CXX_COMPILER=" + hip_comp)
            if self.spec.variants["amd_arch"].value != "none":
                args.append(
                    "-DCXX_EXTRA_FLAGS= --offload-arch="
                    + self.spec.variants["amd_arch"].value
                    + " "
                    + self.spec.variants["flags"].value
                    + " -O3"
                )

        if "sycl" in model:
            os.system("spack load intel-oneapi-compilers")
            args.append("-DSYCL_COMPILER=ONEAPI-DPCPP")

        if "kokkos" in model:
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            args.append("-DKOKKOS_IN_PACKAGE=" + self.spec["kokkos"].prefix)
            if self.spec.satisfies("+cuda"):
                args.append("-DKokkos_ENABLE_CUDA=ON")
            if self.spec.satisfies("+openmp"):
                args.append("-DKokkos_ENABLE_OPENMP=ON")

        if "raja" in model:
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            args.append("-DRAJA_IN_PACKAGE=" + self.spec["raja"].prefix)
            args.append("-DRAJA_DIR=" + self.spec["raja"].prefix + "/share ")
            if self.spec.satisfies("+openmp"):
                args.append("-DENABLE_OPENMP=ON")

        if "tbb" in model:
            args.append("-DTBB_ROOT=" + self.spec["tbb"].prefix + "/lib/cmake/tbb")
            # Hack to get around the fact that TBBConfig.cmake is linking 32bit libs.
            args.append("-DCMAKE_SIZEOF_VOID_P=8")

        return args
