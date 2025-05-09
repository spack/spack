# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neon(CMakePackage):
    """NeoN is a PDE solver for CFD frameworks."""

    homepage = "https://github.com/exasim-project/neon"
    git = "https://github.com/exasim-project/neon.git"

    maintainers("greole", "HenningScheufler")

    license("MIT", checked_by="greole")

    version("main", branch="main")

    variant("cuda", default=False, description="Compile with CUDA support")
    variant("hip", default=False, description="Compile with HIP support")
    variant("omp", default=False, description="Compile with OMP support")
    variant("threads", default=True, description="Compile with Threads support")
    variant("ginkgo", default=True, description="Compile with Ginkgo")
    variant("petsc", default=False, description="Compile with PETSc")
    variant("sundials", default=True, description="Compile with Sundials")
    variant("test", default=False, description="Compile and install tutorial programs")
    variant("adios2", default=False, description="Compile with ADIOS2 support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("mpi@3")
    depends_on("cuda@12.6", when="+cuda")
    depends_on("hip", when="+hip")
    depends_on("kokkos@4.3.00")
    depends_on("ginkgo@develop", when="+ginkgo")
    depends_on("petsc", when="+petsc")
    depends_on("sundials", when="+sundials")
    depends_on("adios2", when="+adios2")

    def cmake_args(self):
        args = [
            self.define_from_variant("NeoN_WITH_GINKGO", "ginkgo"),
            self.define_from_variant("NeoN_WITH_OMP", "omp"),
            self.define_from_variant("NeoN_WITH_THREADS", "threads"),
            self.define_from_variant("NeoN_WITH_ADIOS2", "adios2"),
            self.define_from_variant("NeoN_WITH_SUNDIALS", "sundials"),
            self.define_from_variant("NeoN_WITH_PETSC", "petsc"),
            self.define_from_variant("NeoN_BUILD_TESTS", "test"),
            self.define_from_variant("Kokkos_ENABLE_CUDA", "cuda"),
            self.define_from_variant("Kokkos_ENABLE_HIP", "hip"),
            self.define("CPM_USE_LOCAL_PACKAGES", True),
        ]
        return args
