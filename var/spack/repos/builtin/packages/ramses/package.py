# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ramses(MakefilePackage):
    """Ramses benchmark for DiRAC.

    The source code for this benchmark is stored in a private repository. To
    gain access please contact the RSE team at the University of Leicester or
    contact via github from our organization page
    https://github.com/UniOfLeicester
    """

    homepage = "https://github.com/UniOfLeicester/benchmark-ramses"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-ramses.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="main")

    executables = [r"^ramses3d$"]

    depends_on("mpi")

    parallel = False

    def edit(self, spec, prefix):

        os.chdir(os.path.join(os.getcwd(), "SRC", "bin"))
        makefile = FileFilter("Makefile")
        makefile.filter(r"^PREFIX := .*", f"PREFIX = {prefix}")
        if self.compiler.name == "intel":
            env["I_MPI_F90"] = spack_fc
            fc = spec["mpi"].mpifc
            makefile.filter(r"^F90 = .*", f"F90 = {fc}")
        elif self.compiler.name == "gcc":
            makefile.filter(
                r"^\s*FFLAGS\s*= .*",
                f"FFLAGS = -O3 -cpp -march=core-avx2 -fomit-frame-pointer -ffree-line-length-none",
            )
        else:
            msg = "The compiler you are building with, "
            msg += "'{0}', is not supported by ramses yet."
            raise InstallError(msg.format(self.compiler.name))

    def build(self, spec, prefix):

        make()

    def install(self, spec, prefix):

        make("install")
