# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eigenexa(AutotoolsPackage):
    """EigenExa is a high-performance eigenvalue solver."""

    homepage = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/"
    url = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/EigenExa-2.6.tgz"

    version(
        "2.6", sha256="a1a4e571a8051443f28e7ea4889272993452a4babd036d2b4dd6b28154302f95"
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mpi")
    depends_on("lapack")
    depends_on("scalapack")

    patch("fj_compiler.patch", when="%fj")

    parallel = False

    def setup_build_environment(self, env):
        env.set("FC", self.spec["mpi"].mpifc, force=True)
        env.set("F77", self.spec["mpi"].mpif77, force=True)
        env.set("CC", self.spec["mpi"].mpicc, force=True)
        env.set(
            "LAPACK_LIBS",
            "{0} {1}".format(
                self.spec["lapack"].libs.ld_flags, self.spec["scalapack"].libs.ld_flags
            ),
        )
        env.set(
            "LAPACK_PATH",
            "{0}".format(
                ":".join(
                    self.spec["lapack"].libs.directories
                    + self.spec["scalapack"].libs.directories
                )
            ),
        )
