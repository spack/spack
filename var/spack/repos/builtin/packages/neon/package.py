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
    variant("ginkgo", default=True, description="Compile with Ginkgo")
    variant("petsc", default=False, description="Compile with PETSc")
    variant("sundials", default=True, description="Compile with Sundials")
    variant("test", default=False, description="Compile and install tutorial programs")
    variant("adios2", default=False, description="Compile with ADIOS2 support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("mpi@3")
    depends_on("cuda@12.6", when="+cuda")
    depends_on("kokkos@4.3.00")
    depends_on("ginkgo", when="+ginkgo")
    depends_on("petsc", when="+petsc")
    depends_on("adios2", when="+adios2")

    def cmake_args(self):
        return [
            "-DNeoN_WITH_GINKGO=%s" % ("+ginkgo" in self.spec),
            "-DNeoN_WITH_OMP=%s" % ("+omp" in self.spec),
            "-DNeoN_WITH_THREADS=%s" % ("+omp" not in self.spec),
            "-DNeoN_WITH_PETSC=%s" % ("+petsc" in self.spec),
            "-DNeoN_WITH_SUNDIALS=%s" % ("+sundials" in self.spec),
            "-DNeoN_WITH_ADIOS2=%s" % ("+adios2" in self.spec),
            "-DNeoN_BUILD_TESTS=%s" % ("+test" in self.spec),
            "-DKokkos_ENABLE_CUDA=%s" % ("+cuda" in self.spec),
            "-DKokkos_ENABLE_HIP=%s" % ("+hip" in self.spec),
        ]
