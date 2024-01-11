# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.boost import Boost


class Amp(CMakePackage, CudaPackage, ROCmPackage):
    """The Advanced Multi-Physics (AMP) package.

    The Advanced Multi-Physics (AMP) package is an open source parallel
    object-oriented computational framework that is designed with single
    and multi-domain multi-physics applications in mind.
    """

    homepage = "https://bitbucket.org/AdvancedMultiPhysics/amp"
    git = "https://bitbucket.org/AdvancedMultiPhysics/amp.git"

    version("develop", branch="master")
    version(
        "2.0.0", tag="2.0.0", commit="3c735a0c8a028857940736b1d0bdd1ee2954d326", preferred=True
    )

    variant("boost", default=False, description="Build with support for Boost")
    variant("hdf5", default=False, description="Build with support for HDF5")
    variant("hypre", default=False, description="Build with support for hypre")
    variant("kokkos", default=False, description="Build with support for Kokkos")
    variant("libmesh", default=False, description="Build with libmesh support")
    variant("mpi", default=False, description="Build with MPI support")
    variant("netcdf", default=False, description="Build with NetCDF support")
    variant("petsc", default=False, description="Build with Petsc support")
    variant("shared", default=False, description="Build shared libraries")
    variant("silo", default=False, description="Build with support for Silo")
    variant("sundials", default=False, description="Build with support for Sundials")
    variant("trilinos", default=False, description="Build with support for Trilinos")
    variant("umpire", default=False, description="Build with support for UMPIRE")
    variant("zlib", default=False, description="Build with support for zlib")

    depends_on("git", type="build")

    depends_on("blas")
    depends_on("lapack")

    depends_on("boost", when="+boost")
    depends_on("hdf5", when="+hdf5")
    depends_on("hypre", when="+hypre")
    depends_on("kokkos", when="+kokkos")
    depends_on("libmesh", when="+libmesh")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("petsc", when="+petsc")
    depends_on("silo", when="+silo")
    depends_on("sundials@2.6.2", when="+sundials")
    depends_on(
        "trilinos@13.4.1 +epetra+epetraext+thyra+tpetra+ml+amesos+ifpack+ifpack2+belos+nox+stratimikos cxxstd=17 gotype=int",
        when="+trilinos",
    )
    depends_on("umpire", when="+umpire")
    depends_on("zlib-api", when="+zlib")

    depends_on("trilinos +kokkos", when="+trilinos+kokkos")
    depends_on("trilinos +mpi", when="+trilinos+mpi")

    depends_on("kokkos+cuda+cuda_constexpr", when="+kokkos+cuda")
    depends_on("hypre+cuda+unified-memory", when="+hypre+cuda")
    depends_on("petsc+cuda", when="+petsc+cuda")

    for _flag in list(CudaPackage.cuda_arch_values):
        depends_on("hypre cuda_arch=" + _flag, when="+hypre+cuda cuda_arch=" + _flag)
        depends_on("petsc cuda_arch=" + _flag, when="+petsc+cuda cuda_arch=" + _flag)
        depends_on("kokkos cuda_arch=" + _flag, when="+kokkos+cuda cuda_arch=" + _flag)

    # MPI related dependencies
    depends_on("mpi", when="+mpi")

    resource(
        name="tpl-builder",
        git="https://bitbucket.org/AdvancedMultiPhysics/tpl-builder.git",
        tag="1.0.0",
        commit="b68100657186dcfd236e955eb6c2079a88aa4854",
        destination="downloads",
        when="@2.0.0:",
    )

    def setup_build_environment(self, env):
        if "^kokkos-nvcc-wrapper" in self.spec:
            # undo nvcc wrapper changes
            env.set("MPICH_CXX", spack_cxx)
            env.set("OMPI_CXX", spack_cxx)
            env.set("MPICXX_CXX", spack_cxx)

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define("TPL_URL", join_path(self.stage.source_path, "downloads", "tpl-builder")),
            self.define("AMP_ENABLE_TESTS", False),
            self.define("AMP_ENABLE_EXAMPLES", "OFF"),
            self.define("CXX_STD", "17"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("MPI_COMPILER", "mpi"),
        ]

        if "+cuda" in spec:
            cuda_arch = self.spec.variants["cuda_arch"].value
            if cuda_arch[0] != "none":
                options.extend(
                  [
                    self.define("USE_CUDA", True),
                    self.define("CMAKE_CUDA_COMPILER", join_path(spec["cuda"].prefix.bin, "nvcc")),
                    self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch),
                    self.define("CMAKE_CUDA_FLAGS", "-extended-lambda --expt-relaxed-constexpr")
                  ]
                )

        if "+mpi" in spec:
            options.extend(
                [
                    self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    self.define("MPIEXEC", spec["mpi"].prefix.bin),
                ]
            )
        else:
            options.extend(
                [
                    self.define("CMAKE_C_COMPILER", self.compiler.cc),
                    self.define("CMAKE_CXX_COMPILER", self.compiler.cxx),
                    self.define("CMAKE_Fortran_COMPILER", self.compiler.fc),
                ]
            )

        tpl_list = ["LAPACK"]
        blas, lapack = spec["blas"].libs, spec["lapack"].libs
        options.extend(
            [
                self.define("TPL_LAPACK_INSTALL_DIR", spec["lapack"].prefix.mkl),
                self.define("TPL_BLAS_LIBRARY_NAMES", ";".join(blas.names)),
                self.define("TPL_BLAS_LIBRARY_DIRS", ";".join(blas.directories)),
                self.define("TPL_LAPACK_LIBRARY_NAMES", ";".join(lapack.names)),
                self.define("TPL_LAPACK_LIBRARY_DIRS", ";".join(lapack.directories)),
            ]
        )

        if "+zlib" in spec:
            tpl_list.append("ZLIB")
            options.append(self.define("TPL_ZLIB_INSTALL_DIR", spec["zlib-api"].prefix))

        for vname in (
            "boost",
            "hdf5",
            "hypre",
            "kokkos",
            "libmesh",
            "petsc",
            "silo",
            "sundials",
            "trilinos",
            "umpire",
        ):
            if "+" + vname in spec:
                tpl_list.append(vname.upper())
                options.append(self.define(f"TPL_{vname.upper()}_INSTALL_DIR", spec[vname].prefix))

        if "+netcdf" in spec:
            tpl_list.append("NETCDF")
            options.append(self.define("TPL_NETCDF_INSTALL_DIR", spec["netcdf-c"].prefix))

        options.append(self.define("TPL_LIST", ";".join(tpl_list)))
        return options
