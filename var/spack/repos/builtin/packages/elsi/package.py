# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Elsi(CMakePackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    url = "https://wordpress.elsi-interchange.org/wp-content/uploads/2019/03/elsi-2.2.1.tar.gz"

    license("BSD-3-Clause")

    version("2.2.1", sha256="5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d")

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
    variant("use_external_elpa", default=False, description="Build ELPA using SPACK")
    variant("use_external_ntpoly", default=False, description="Build NTPoly using SPACK")
    variant("use_external_omm", default=False, description="Use external libOMM and MatrixSwitch")
    variant("use_external_superlu", default=False, description="Use external SuperLU DIST")
    variant(
        "use_mpi_iallgather", default=True, description="Use non-blocking collective MPI functions"
    )

    # Basic dependencies
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("cmake", type="build")
    depends_on("mpi")
    depends_on("scalapack", type="link")

    # Library dependencies
    depends_on("elpa", when="+use_external_elpa")
    depends_on("ntpoly", when="+use_external_ntpoly")
    depends_on("slepc", when="+enable_sips")
    depends_on("petsc", when="+enable_sips")
    depends_on("superlu-dist", when="+use_external_superlu")

    def cmake_args(self):
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
            self.define_from_variant("USE_EXTERNAL_OMM", "use_external_omm"),
            self.define_from_variant("USE_EXTERNAL_SUPERLU", "use_external_superlu"),
            self.define_from_variant("USE_MPI_IALLGATHER", "use_mpi_iallgather"),
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
