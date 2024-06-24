# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Elsi(CMakePackage, CudaPackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    url = "https://gitlab.com/elsi_project/elsi_interface/-/archive/v2.10.1/elsi_interface-v2.10.1.tar.gz"
    git = "https://gitlab.com/elsi_project/elsi_interface.git"

    license("BSD-3-Clause")

    version("2.10.1", sha256="b3c7526d46a9139a26680787172a3df15bc648715a35bdf384053231e94ab829")
    version("2.2.1", sha256="5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d")
    version("master", branch="master")

    variant("add_underscore", default=True, description="Suffix C functions with an underscore")
    variant(
        "elpa2_kernel",
        default="none",
        description="ELPA2 Kernel",
        values=("none", "AVX", "AVX2", "AVX512"),
        multi=False,
    )
    variant("enable_pexsi", default=False, description="Enable PEXSI support")
    variant("enable_sips", default=False, description="Enable SLEPc-SIPs support")
    variant("use_external_elpa", default=True, description="Build ELPA using SPACK")
    variant("use_external_ntpoly", default=True, description="Build NTPoly using SPACK")
    variant("use_external_superlu", default=True, description="Use external SuperLU DIST")
    variant(
        "use_mpi_iallgather", default=True, description="Use non-blocking collective MPI functions"
    )
    variant(
        "internal_elpa_version",
        default="2024",
        values=("2024", "2023_11", "2023", "2021", "2020"),
        description="Internal ELPA version",
        multi=False,
    )

    # Basic dependencies
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", type="link")
    depends_on("mpi")

    # Library dependencies
    with when("+use_external_elpa"):
        depends_on("elpa+cuda", when="+cuda")
        depends_on("elpa~cuda", when="~cuda")
    depends_on("ntpoly", when="+use_external_ntpoly")
    with when("+enable_sips"):
        depends_on("slepc+cuda", when="+cuda")
        depends_on("slepc~cuda", when="~cuda")
        depends_on("petsc+cuda", when="+cuda")
        depends_on("petsc~cuda", when="~cuda")
    with when("+use_external_superlu"):
        depends_on("superlu-dist+cuda", when="+cuda")
        depends_on("superlu-dist~cuda", when="~cuda")

    def cmake_args(self):
        libs_names = ["scalapack", "lapack", "blas"]

        # External libraries
        if self.spec.satisfies("+use_external_elpa"):
            libs_names.append("elpa")
        if self.spec.satisfies("+use_external_ntpoly"):
            libs_names.append("ntpoly")
        if self.spec.satisfies("+use_external_superlu"):
            libs_names.append("superlu-dist")

        lib_paths, libs = [], []
        for lib in libs_names:
            lib_paths.extend(self.spec[lib].libs.directories)
            libs.extend(self.spec[lib].libs.names)

        args = [
            # Compiler Information (ELSI wants these explicitly set)
            self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc),
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
            self.define_from_variant("ADD_UNDERSCORE", "add_underscore"),
            self.define_from_variant("ENABLE_PEXSI", "enable_pexsi"),
            self.define_from_variant("ENABLE_SIPS", "enable_sips"),
            self.define_from_variant("USE_EXTERNAL_ELPA", "use_external_elpa"),
            self.define_from_variant("USE_EXTERNAL_NTPOLY", "use_external_ntpoly"),
            self.define_from_variant("USE_EXTERNAL_SUPERLU", "use_external_superlu"),
            self.define_from_variant("USE_MPI_IALLGATHER", "use_mpi_iallgather"),
            self.define("ENABLE_TESTS", self.run_tests),
            self.define("ENABLE_C_TESTS", self.run_tests),
            self.define_from_variant("USE_GPU_CUDA", "cuda"),
            self.define("LIB_PATHS", ";".join(lib_paths)),
            self.define("LIBS", ";".join(libs)),
            self.define(f"USE_ELPA_{self.spec.variants['internal_elpa_version'].value}", True),
        ]

        if self.spec.variants["elpa2_kernel"].value != "none":
            args.append(self.define_from_variant("ELPA2_KERNEL", "elpa2_kernel"))

        if self.spec.satisfies("+use_external_elpa"):
            elpa_module = find(self.spec["elpa"].prefix, "elpa.mod")
            args.append(self.define("INC_PATHS", os.path.dirname(elpa_module[0])))

        # Only when using fujitsu compiler
        if self.spec.satisfies("%fj"):
            args.append(self.define("CMAKE_Fortran_MODDIR_FLAG", "-M"))

        return args
