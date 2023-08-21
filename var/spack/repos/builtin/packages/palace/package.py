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

    maintainers("sebastiangrimberg")

    version("develop", branch="main")
    version("0.11.2", tag="v0.11.2")

    variant("shared", default=True, description="Enables the build of shared libraries")
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
    depends_on("pkgconfig", type="build")
    depends_on("mpi")
    depends_on("zlib-api")
    depends_on("nlohmann-json")
    depends_on("fmt")
    depends_on("eigen")

    depends_on("metis@5:")
    depends_on("metis+shared", when="+shared")
    depends_on("metis~shared", when="~shared")
    depends_on("metis+int64", when="+int64")
    depends_on("metis~int64", when="~int64")

    depends_on("hypre~complex")
    depends_on("hypre+shared", when="+shared")
    depends_on("hypre~shared", when="~shared")
    depends_on("hypre+mixedint", when="+int64")
    depends_on("hypre~mixedint", when="~int64")
    depends_on("hypre+openmp", when="+openmp")
    depends_on("hypre~openmp", when="~openmp")

    with when("+superlu-dist"):
        depends_on("superlu-dist+shared", when="+shared")
        depends_on("superlu-dist~shared", when="~shared")
        depends_on("superlu-dist+int64", when="+int64")
        depends_on("superlu-dist~int64", when="~int64")
        depends_on("superlu-dist+openmp", when="+openmp")
        depends_on("superlu-dist~openmp", when="~openmp")

    with when("+strumpack"):
        depends_on("strumpack+butterflypack+zfp+parmetis")
        depends_on("strumpack+shared", when="+shared")
        depends_on("strumpack~shared", when="~shared")
        depends_on("strumpack+openmp", when="+openmp")
        depends_on("strumpack~openmp", when="~openmp")

    with when("+mumps"):
        depends_on("mumps+metis+parmetis")
        depends_on("mumps+shared", when="+shared")
        depends_on("mumps~shared", when="~shared")
        depends_on("mumps+openmp", when="+openmp")
        depends_on("mumps~openmp", when="~openmp")

    with when("+slepc"):
        depends_on("slepc ^petsc+mpi+double+complex")
        depends_on("petsc+shared", when="+shared")
        depends_on("petsc~shared", when="~shared")
        depends_on("petsc+int64", when="+int64")
        depends_on("petsc~int64", when="~int64")
        depends_on("petsc+openmp", when="+openmp")
        depends_on("petsc~openmp", when="~openmp")

    with when("+arpack"):
        depends_on("arpack-ng+mpi+icb@develop")
        depends_on("arpack-ng+shared", when="+shared")
        depends_on("arpack-ng~shared", when="~shared")

    # Palace always builds its own internal MFEM, GSLIB
    conflicts("mfem")
    conflicts("gslib")

    # More dependency variant conflicts
    conflicts("^hypre+int64", msg="Palace uses HYPRE's mixedint option for 64 bit integers")
    conflicts("^mumps+int64", msg="Palace requires MUMPS without 64 bit integers")
    conflicts("^slepc+arpack", msg="Palace requires SLEPc without ARPACK")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PALACE_WITH_64BIT_INT", "int64"),
            self.define_from_variant("PALACE_WITH_OPENMP", "openmp"),
            self.define_from_variant("PALACE_WITH_GSLIB", "gslib"),
            self.define_from_variant("PALACE_WITH_SUPERLU", "superlu-dist"),
            self.define_from_variant("PALACE_WITH_STRUMPACK", "strumpack"),
            self.define_from_variant("PALACE_WITH_MUMPS", "mumps"),
            self.define_from_variant("PALACE_WITH_SLEPC", "slepc"),
            self.define_from_variant("PALACE_WITH_ARPACK", "arpack"),
            self.define("PALACE_BUILD_EXTERNAL_DEPS", False),
        ]

        # HYPRE is always built with external BLAS/LAPACK
        args += [
            self.define("HYPRE_REQUIRED_PACKAGES", "LAPACK;BLAS"),
            self.define("BLAS_LIBRARIES", "{0}".format(self.spec["blas"].libs.joined(";"))),
            self.define("LAPACK_LIBRARIES", "{0}".format(self.spec["lapack"].libs.joined(";"))),
        ]

        # MPI compiler wrappers are not required, but MFEM test builds need to know to link
        # against MPI libraries
        if "+superlu-dist" in self.spec:
            args += [self.define("SuperLUDist_REQUIRED_PACKAGES", "LAPACK;BLAS;MPI")]
        if "+strumpack" in self.spec:
            args += [self.define("STRUMPACK_REQUIRED_PACKAGES", "LAPACK;BLAS;MPI;MPI_Fortran")]
        if "+mumps" in self.spec:
            args += [self.define("MUMPS_REQUIRED_PACKAGES", "LAPACK;BLAS;MPI;MPI_Fortran")]

        return args

    def install(self, spec, prefix):
        # No install phase for Palace (always performed during build)
        pass
