# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TrovePdsyev(MakefilePackage):
    """trove-pdsyev benchmark for DiRAC.

    The source code for this benchmark is stored in a private repository. To
    gain access please contact the RSE team at the University of Leicester or
    contact via github from our organization page
    https://github.com/UniOfLeicester
    """

    homepage = "https://github.com/UniOfLeicester/benchmark-trove-pdsyev"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove-pdsyev.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="main")

    variant("ipp", default=True, description="enable use of intel optimized headers")

    executables = [r"^diag_generic.x$"]

    depends_on("mpi")
    depends_on("mkl")
    depends_on("ipp", when="+ipp")

    parallel = False

    def edit(self, spec, prefix):

        if self.compiler.name != "intel":
            msg = "The compiler [{self.compiler.name}] is not supported yet."
            raise InstallError(msg)

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env["DESTDIR"] = ""
        env["PREFIX"] = prefix
        env["I_MPI_F90"] = spack_fc

        makefile = FileFilter("Makefile")
        makefile.filter(r"PLAT\s*=.*", "PLAT = _generic")
        makefile.filter(r"FOR\s*= .*", f"FOR = {self.fc}")
        LIB = (
            "-lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core "
            "-lmkl_blacs_intelmpi_lp64 -liomp5 -lpthread -lm -ldl"
        )
        makefile.filter(r"LIB\s*= .*", f"LIB = {LIB}")

        if "~ipp" in spec:
            makefile.filter(r"(.*) -use-intel-optimized-headers (.*)", r"\1 \2")

    def build(self, spec, prefix):

        make()

    def install(self, spec, prefix):

        make("install")
