# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Nlcglib(CMakePackage, CudaPackage, ROCmPackage):
    """Nonlinear CG methods for wave-function optimization in DFT."""

    homepage = "https://github.com/simonpintarelli/nlcglib"
    git = "https://github.com/simonpintarelli/nlcglib.git"
    url = "https://github.com/simonpintarelli/nlcglib/archive/v0.9.tar.gz"

    maintainers("simonpintarelli")

    license("BSD-3-Clause")

    version("develop", branch="develop")

    version("1.1.0", sha256="9e7c2eea84a5ce191bd9af08f6c890717f7b6e88be7bd15cfe774eb0e0dabd8a")
    version("1.0b", sha256="086c46f06a117f267cbdf1df4ad42a8512689a9610885763f463469fb15e82dc")
    version("0.9", sha256="8d5bc6b85ee714fb3d6480f767e7f43e5e7d569116cf60e48f533a7f50a37a08")

    variant("openmp", default=True, description="Use OpenMP")
    variant("tests", default=False, description="Build tests")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    with when("@1.1: +cuda"):
        variant(
            "gpu_direct",
            default=False,
            description="Enable GPU direct. Required to support distributed wave-functions.",
        )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.21:", type="build")
    depends_on("mpi")
    depends_on("lapack")

    requires(
        "^[virtuals=lapack] openblas",
        "^[virtuals=lapack] intel-oneapi-mkl",
        policy="one_of",
        msg="Only mkl or openblas are supported for blas/lapack with ldak",
    )

    depends_on("kokkos~cuda~rocm", when="~cuda~rocm")
    depends_on("kokkos+openmp", when="+openmp")

    depends_on("googletest", type="build", when="+tests")
    depends_on("nlohmann-json")
    depends_on("kokkos@4:", when="@1.1:")

    # MKLConfig.cmake introduced in 2021.3
    conflicts("intel-oneapi-mkl@:2021.2", when="^intel-oneapi-mkl")

    with when("@:0.9"):
        conflicts("+rocm")
        conflicts("^kokkos@4:")

    with when("+rocm"):
        variant("magma", default=True, description="Use magma eigenvalue solver (AMDGPU)")
        depends_on("magma+rocm", when="+magma")
        depends_on("kokkos+rocm")
        depends_on("rocblas")
        depends_on("rocsolver")

    with when("+cuda"):
        depends_on("kokkos+cuda_lambda+wrapper", when="%gcc")
        depends_on("kokkos+cuda")
        for arch in CudaPackage.cuda_arch_values:
            depends_on(f"kokkos cuda_arch={arch}", when=f"cuda_arch={arch}")

    def cmake_args(self):
        options = [
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define_from_variant("BUILD_TESTS", "tests"),
            self.define_from_variant("USE_ROCM", "rocm"),
            self.define_from_variant("USE_GPU_DIRECT", "gpu_direct"),
            self.define_from_variant("USE_MAGMA", "magma"),
            self.define_from_variant("USE_CUDA", "cuda"),
        ]

        if self.spec.satisfies("^[virtuals=lapack] intel-oneapi-mkl"):
            mkl_mapper = {
                "threading": {"none": "sequential", "openmp": "gnu_thread", "tbb": "tbb_thread"},
                "mpi": {"intel-oneapi-mpi": "intelmpi", "mpich": "mpich", "openmpi": "openmpi"},
            }

            mkl_threads = mkl_mapper["threading"][
                self.spec["intel-oneapi-mkl"].variants["threads"].value
            ]

            mpi_provider = self.spec["mpi"].name
            if mpi_provider in ["mpich", "cray-mpich", "mvapich", "mvapich2"]:
                mkl_mpi = mkl_mapper["mpi"]["mpich"]
            else:
                mkl_mpi = mkl_mapper["mpi"][mpi_provider]

            options.extend(
                [
                    self.define("LAPACK_VENDOR", "MKLONEAPI"),
                    self.define("MKL_INTERFACE", "lp64"),
                    self.define("MKL_THREADING", mkl_threads),
                    self.define("MKL_MPI", mkl_mpi),
                ]
            )

        else:
            options.append(self.define("LAPACK_VENDOR", "OpenBLAS"))

        if "+cuda%gcc" in self.spec:
            options.append(
                self.define("CMAKE_CXX_COMPILER", self["kokkos-nvcc-wrapper"].kokkos_cxx)
            )

        if "+cuda" in self.spec:
            cuda_archs = self.spec.variants["cuda_arch"].value
            if "@:0.9" in self.spec:
                cuda_flags = " ".join(
                    ["-gencode arch=compute_{0},code=sm_{0}".format(x) for x in cuda_archs]
                )
                options.append(self.define("CMAKE_CUDA_FLAGS", cuda_flags))
            else:
                options.append(self.define("CMAKE_CUDA_ARCHITECTURES", cuda_archs))

        if "^cuda+allow-unsupported-compilers" in self.spec:
            options.append(self.define("CMAKE_CUDA_FLAGS", "--allow-unsupported-compiler"))

        if "+rocm" in self.spec:
            archs = ",".join(self.spec.variants["amdgpu_target"].value)
            options.extend(
                [
                    self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc),
                    self.define("HIP_HCC_FLAGS", f"--amdgpu-target={archs}"),
                    self.define(
                        "CMAKE_CXX_FLAGS", f"--amdgpu-target={archs} --offload-arch={archs}"
                    ),
                ]
            )

        return options
