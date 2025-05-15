# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#


from spack.package import *


class Dplasma(CMakePackage, CudaPackage):
    """DPLASMA is a highly optimized, accelerator-aware, implementation of a
    dense linear algebra package for distributed heterogeneous systems. It is
    designed to deliver sustained performance for distributed systems where each
    node featuring multiple sockets of multicore processors, and if available,
    accelerators, using the PaRSEC runtime as a backend."""

    homepage = "https://github.com/ICLDisco/dplasma"
    git = "https://github.com/ICLDisco/dplasma.git"
    maintainers("G-Ragghianti", "abouteiller", "bosilca", "herault")

    license("BSD-3-Clause-Open-MPI")

    version("develop", branch="master")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    variant("shared", default=True, description="Build a shared library")
    variant("cuda", default=True, description="Build with CUDA")
    variant("internal-parsec", default="False", description="Build with internal PaRSEC")

    depends_on("c", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("python", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("hwloc")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("parsec+cuda", when="~internal-parsec+cuda")
    depends_on("parsec~cuda", when="~internal-parsec~cuda")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_BUILD_TYPE", "build_type"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("DPLASMA_GPU_WITH_CUDA", "cuda"),
            self.define("DPLASMA_GPU_WITH_HIP", "Off"),
        ]
        if "~internal-parsec" in self.spec:
            args.append(self.define("PaRSEC_ROOT", self.spec["parsec"].prefix))
        return args
