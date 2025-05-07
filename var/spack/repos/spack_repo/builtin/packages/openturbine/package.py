# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openturbine(CMakePackage, CudaPackage, ROCmPackage):
    """An open-source wind turbine structural dynamics simulation code."""

    license("MIT License", checked_by="ddement")

    homepage = "https://www.exascaleproject.org/research-project/exawind/"
    url = "https://github.com/Exawind/openturbine.git"
    git = "https://github.com/Exawind/openturbine.git"

    maintainers("faisal-bhuiyan", "ddement", "deslaughter")

    version("main", branch="main")

    variant("tests", default=False, description="Build OpenTurbine Test Suite")
    variant("openmp", default=False, description="Build OpenTurbine with OpenMP support")
    variant("vtk", default=False, description="Enable VTK")
    variant("adi", default=False, description="Build the OpenFAST ADI external project")
    variant("rosco", default=False, description="Build the ROSCO controller external project")
    variant("klu", default=True, description="Build with support for the KLU sparse direct solver")
    variant(
        "umfpack",
        default=False,
        description="Build with support for the UMFPACK sparse direct solver",
    )
    variant(
        "superlu",
        default=False,
        description="Build with support for the SuperLU sparse direct solver",
    )
    variant(
        "superlu-mt",
        default=False,
        description="Build with support for the SuperLU_MT sparse direct solver",
    )
    variant(
        "mkl",
        default=False,
        description="Build with support for the MKL Pardiso sparse direct solver",
    )
    variant(
        "cusolversp",
        default=True,
        when="+cuda",
        description="Build with support for the cuSolverSP sparse direct solver",
    )

    depends_on("cxx", type="build")
    depends_on("netcdf-c")
    depends_on("yaml-cpp")
    depends_on("kokkos-kernels")
    depends_on("lapack")

    depends_on("kokkos@4.6:")
    depends_on("kokkos-kernels@4.6:")

    depends_on("kokkos+cuda+wrapper", when="+cuda")
    depends_on("kokkos+rocm", when="+rocm")
    depends_on("kokkos~cuda", when="~cuda")
    depends_on("kokkos~rocm", when="~rocm")

    depends_on("kokkos-kernels+cuda+cublas+cusparse+cusolver", when="+cuda")
    depends_on("kokkos-kernels+rocblas+rocsparse+rocsolver", when="+rocm")
    depends_on("kokkos-kernels+openmp", when="+openmp")
    depends_on("kokkos-kernels~cuda", when="~cuda")
    depends_on("kokkos-kernels~openmp", when="~openmp")

    depends_on("suite-sparse", when="+klu")
    depends_on("suite-sparse", when="+umfpack")
    depends_on("superlu", when="+superlu")
    depends_on("superlu-mt", when="+superlu-mt")
    depends_on("mkl", when="+mkl")

    depends_on("googletest", when="+tests")

    depends_on("fortran", type="build", when="+adi")

    depends_on("fortran", type="build", when="+rosco")

    def cmake_args(self):
        options = [
            self.define_from_variant("OpenTurbine_ENABLE_TESTS", "tests"),
            self.define_from_variant("OpenTurbine_BUILD_OPENFAST_ADI", "adi"),
            self.define_from_variant("OpenTurbine_BUILD_ROSCO_CONTROLLER", "rosco"),
            self.define_from_variant("OpenTurbine_ENABLE_KLU", "klu"),
            self.define_from_variant("OpenTurbine_ENABLE_UMFPACK", "umfpack"),
            self.define_from_variant("OpenTurbine_ENABLE_SUPERLU", "superlu"),
            self.define_from_variant("OpenTurbine_ENABLE_SUPERLU_MT", "superlu-mt"),
            self.define_from_variant("OpenTurbine_ENABLE_MKL", "mkl"),
            self.define_from_variant("OpenTurbine_ENABLE_CUSOLVERSP", "cusolversp"),
        ]
        return options
