# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trove(MakefilePackage):
    """trove benchmark for DiRAC.

    The source code for this benchmark is stored in a private repository. To
    gain access please contact the RSE team at the University of Leicester or
    contact via github from our organization page
    https://github.com/UniOfLeicester
    """

    homepage = "https://github.com/UniOfLeicester/benchmark-trove"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="update-makefile")

    executables = [r"^j-trove.x$"]

    depends_on("mpi")
    depends_on("mkl")

    parallel = False

    def edit(self, spec, prefix):

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env["PREFIX"] = prefix
        env["FOR"] = self.fc
        lapack = "-mkl=parallel -lmkl_scalapack_lp64 " "-lmkl_blacs_intelmpi_lp64 -lmkl_intel_lp64"

        if self.compiler.name == "intel":
            fflags = " -mavx2 -mfma -O3 -ip -Ofast"
            if "openmpi" in spec:
                lapack = (
                    "-mkl=parallel -lmkl_scalapack_lp64 -lmkl_blacs_openmpi_lp64 -lmkl_intel_lp64"
                )

        elif self.compiler.name == "gcc":
            fflags = " -ffree-line-length-none -march=native -O3 " "-fcray-pointer -g3"

            if "openmpi" in spec:
                lapack = (
                    "-lmkl_scalapack_lp64 -lmkl_blacs_openmpi_lp64 -lmkl_gf_lp64 -lmkl_gnu_thread "
                    "-lmkl_core"
                )
        else:
            msg = "The compiler [{self.compiler.name}] is not supported yet."
            raise InstallError(msg)

        env["FFLAGS"] = self.compiler.openmp_flag + fflags
        env["LAPACK"] = lapack

    def build(self, spec, prefix):

        make("goal")

    def install(self, spec, prefix):

        make("install")
