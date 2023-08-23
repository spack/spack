# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amg2023(MakefilePackage):
    """AMG2023 is a parallel algebraic multigrid solver for linear systems
    arising from problems on unstructured grids. The driver provided here
    builds linear systems for various 3-dimensional problems. It requires
    an installation of hypre-2.27.0 or higher.
    """

    tags = ["benchmark"]
    homepage = "https://github.com/LLNL/AMG2023"
    git = "https://github.com/LLNL/AMG2023.git"

    version("develop", branch="main")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("caliper", default=False, description="Enable Caliper monitoring")
    variant("adiak", default=False, description="Enable Adiak metadata gathering")

    depends_on("caliper", when="+caliper")
    depends_on("adiak", when="+adiak")
    depends_on("hypre+caliper", when="+caliper")
    depends_on("hypre@2.27.0:")
    depends_on("mpi", when="+mpi")

    def flag_handler(self, name, flags):
        if name == "ldlibs":
            if self.spec.satisfies("+caliper"):
                flags.append("-lcaliper")
            if self.spec.satisfies("+adiak"):
                flags.append("-ladiak")
        return (flags, None, None)

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        if "+mpi" in spec:
            makefile.filter(r"CC\s*=.*", f"CC = {spec['mpi'].mpicc}")
            makefile.filter(r"CXX\s*=.*", f"CXX = {spec['mpi'].mpicxx}")
            makefile.filter(r"#MPIPATH = .*", f"MPIPATH = {spec['mpi'].prefix}")
            makefile.filter(r"#MPIINCLUDE", "MPIINCLUDE")
            if spec["mpi"].extra_attributes and "ldflags" in spec["mpi"].extra_attributes:
                makefile.filter(
                    "#MPILIBS    = .*",
                    "MPILIBS    = {0}".format(spec["mpi"].extra_attributes["ldflags"]),
                )
            else:
                makefile.filter("#MPILIBDIRS", "MPILIBDIRS")
                makefile.filter("#MPILIBS", "MPILIBS")
            makefile.filter("#MPIFLAGS", "MPIFLAGS")
        else:
            makefile.filter(r"CC\s*=.*", "CC = {0}".format(spack_cc))
            makefile.filter(r"CXX\s*=.*", "CXX = {0}".format(spack_cxx))

        makefile.filter(r"HYPRE_DIR = .*", f'HYPRE_DIR = {spec["hypre"].prefix}')

        if spec["hypre"].satisfies("+cuda"):
            makefile.filter(
                "HYPRE_CUDA_PATH    = .*", "HYPRE_CUDA_PATH    = %s" % (spec["cuda"].prefix)
            )
            makefile.filter("HYPRE_CUDA_INCLUDE = #", "HYPRE_CUDA_INCLUDE = ")
            makefile.filter("HYPRE_CUDA_LIBS    = #", "HYPRE_CUDA_LIBS    = ")
            makefile.filter("HYPRE_HIP_PATH    =", "#HYPRE_HIP_PATH    =")
            makefile.filter("HYPRE_HIP_INCLUDE =", "#HYPRE_HIP_INCLUDE =")
            makefile.filter("HYPRE_HIP_LIBS    =", "#HYPRE_HIP_LIBS    =")

        if spec["hypre"].satisfies("+rocm"):
            makefile.filter("HYPRE_HIP_PATH    = .*", "HYPRE_HIP_PATH    = ${ROCM_PATH}")
        else:
            makefile.filter("HYPRE_HIP_PATH    =", "#HYPRE_HIP_PATH    =")
            makefile.filter("HYPRE_HIP_INCLUDE =", "#HYPRE_HIP_INCLUDE =")
            makefile.filter("HYPRE_HIP_LIBS    =", "#HYPRE_HIP_LIBS    =")

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install("amg", prefix.bin)
