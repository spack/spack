# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Sphng(MakefilePackage):
    """sphNG benchmark for DiRAC.

    The source code for this benchmark is stored in a private repository. To
    gain access please contact the RSE team at the University of Leicester or
    contact via github from our organization page
    https://github.com/UniOfLeicester
    """

    homepage = "https://github.com/UniOfLeicester/benchmark-sphng"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-sphng.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="update-makefile")

    executables = [r"^sph_tree_rk_gradh$"]

    depends_on("mpi")

    parallel = False

    def edit(self, spec, prefix):

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env["PREFIX"] = prefix
        env["SYSTEM"] = "SPACK"
        env["mpi"] = "yes"
        env["openmp"] = "yes"

        env["FC"] = self.fc
        env["OMPFLAG"] = self.compiler.openmp_flag
        if self.compiler.name == "intel":
            env[
                "FFLAGS"
            ] = "-O3 -mavx2 -mfma -mcmodel=medium -warn uninitialized -warn truncated_source -warn interfaces -nogen-interfaces -DINCMPI"
            env["DBLFLAG"] = "-r8"
            env["DEBUGFLAG"] = "-check all -traceback -g -fpe0 -fp-stack-check -heap-arrays -O0"
            env["ENDIANFLAGBIG"] = "-convert big_endian"
            env["ENDIANFLAGLITTLE"] = "-convert little_endian"
        elif self.compiler.name == "gcc":
            env[
                "FFLAGS"
            ] = "-m64 -mcmodel=large -O3 -I. -Wall -Wno-conversion -Wno-unused-dummy-argument -Wno-maybe-uninitialized -Warray-temporaries"
            env["DBLFLAG"] = "-fdefault-real-8 -fdefault-double-8"
            env["DEBUGFLAG"] = "-g"
            env["ENDIANFLAGBIG"] = "-fconvert=big-endian"
            env["ENDIANFLAGLITTLE"] = "-fconvert=little-endian"
        else:
            msg = "The compiler you are building with, "
            msg += "'{0}', is not supported by sphng yet."
            raise InstallError(msg.format(self.compiler.name))

    def build(self, spec, prefix):

        make("gradhrk")

    def install(self, spec, prefix):

        make("install")
