# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Palace(CMakePackage):
    """3D finite element solver for computational electromagnetics"""

    tags = ["cem", "fem", "finite-elements", "hpc", "solver"]

    homepage = "https://github.com/awslabs/palace"
    git = "https://github.com/awslabs/palace.git"

    root_cmakelists_dir = "palace"

    maintainers("sebastiangrimberg")

    version("develop", branch="main")
    version("0.11.0", tag="v0.11.0")

    variant("int64", default=False, description="Use 64 bit integers")
    variant("openmp", default=False, description="Use OpenMP")
    variant(
        "gslib",
        default=True,
        description="Build with GSLIB library for high-order field interpolation",
    )
    variant(
        "superlu-dist", default=True, description="Build with SuperLU_DIST sparse direct solver"
    )
    variant("strumpack", default=False, description="Build with STRUMPACK sparse direct solver")
    variant("mumps", default=False, description="Build with MUMPS sparse direct solver")
    variant("slepc", default=True, description="Build with SLEPc eigenvalue solver")
    variant("arpack", default=False, description="Build with ARPACK eigenvalue solver")

    # Dependencies
    depends_on("cmake@3.13:", type="build")
    depends_on("pkg-config", type="build")
    depends_on("mpi")
    depends_on("zlib")
    depends_on("nlohmann-json")
    depends_on("fmt")

    depends_on("metis@5:+int64", when="+int64")
    depends_on("metis@5:~int64", when="~int64")

    depends_on("hypre+shared")
    depends_on("hypre+mixedint", when="+int64")
    depends_on("hypre~mixedint", when="~int64")
    depends_on("hypre+openmp", when="+openmp")
    depends_on("hypre~openmp", when="~openmp")

    depends_on("petsc+double+complex")
    depends_on("petsc+int64", when="+int64")
    depends_on("petsc~int64", when="~int64")
    depends_on("petsc+openmp", when="+openmp")
    depends_on("petsc~openmp", when="~openmp")

    depends_on("slepc", when="+slepc")
    depends_on("arpack-ng+icb@develop", when="+arpack")
    depends_on("gslib", when="+gslib")

    with when("+superlu-dist"):
        depends_on("superlu-dist+int64", when="+int64")
        depends_on("superlu-dist~int64", when="~int64")
        depends_on("superlu-dist+openmp", when="+openmp")
        depends_on("superlu-dist~openmp", when="~openmp")

    with when("+strumpack"):
        depends_on("strumpack+butterflypack+zfp+parmetis")
        depends_on("strumpack+openmp", when="+openmp")
        depends_on("strumpack~openmp", when="~openmp")

    with when("+mumps"):
        depends_on("mumps+metis+parmetis")
        depends_on("mumps+openmp", when="+openmp")
        depends_on("mumps~openmp", when="~openmp")

    # Conflicts: Palace always builds its own internal MFEM
    conflicts("^mfem", msg="Palace builds its own internal MFEM")

    # More dependency variant conflicts
    conflicts("^hypre+int64", msg="Palace uses HYPRE's mixedint option for 64 bit integers")
    conflicts("^petsc~double", msg="Palace requires PETSc with double precision")
    conflicts("^petsc~complex", msg="Palace requires PETSc with complex numbers")
    conflicts("^petsc+metis", msg="Palace requires PETSc without METIS")
    conflicts("^petsc+hypre", msg="Palace requires PETSc without HYPRE")
    conflicts("^petsc+superlu-dist", msg="Palace requires PETSc without SuperLU_DIST")
    conflicts("^slepc+arpack", msg="Palace requires SLEPc without ARPACK")
    conflicts("^mumps+int64", msg="Palace requires MUMPS without 64 bit integers")

    def cmake_args(self):
        args = [
            self.define_from_variant("PALACE_WITH_OPENMP", "openmp"),
            self.define_from_variant("PALACE_WITH_GSLIB", "gslib"),
            self.define_from_variant("PALACE_WITH_SUPERLU", "superlu-dist"),
            self.define_from_variant("PALACE_WITH_STRUMPACK", "strumpack"),
            self.define_from_variant("PALACE_WITH_MUMPS", "mumps"),
            self.define_from_variant("PALACE_WITH_SLEPC", "slepc"),
            self.define_from_variant("PALACE_WITH_ARPACK", "arpack"),
            "-DPALACE_WITH_INTERNAL_JSON=OFF",
            "-DPALACE_WITH_INTERNAL_FMT=OFF",
        ]

        # MPI compiler wrappers are not required, but MFEM test builds need to know to link
        # against MPI libraries
        if "+superlu-dist" in self.spec:
            args += ["-DSuperLUDist_REQUIRED_PACKAGES=MPI"]
        if "+strumpack" in self.spec:
            args += ["-DSTRUMPACK_REQUIRED_PACKAGES=MPI;MPI_Fortran"]
        if "+mumps" in self.spec:
            args += ["-DMUMPS_REQUIRED_PACKAGES=MPI;MPI_Fortran"]

        # HYPRE is always built with external BLAS/LAPACK
        args += ["-DHYPRE_REQUIRED_PACKAGES=LAPACK;BLAS"]

        return args
