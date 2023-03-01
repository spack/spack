# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Trove(MakefilePackage):
    """trove benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-trove"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="update-makefile")
    # version("v1.0.0", tag="v1.0.0")

    executables = [r"^j-trove.x$"]

    depends_on("mpi")
    depends_on("intel-oneapi-mkl")

    parallel=False

    def edit(self, spec, prefix):

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env['PREFIX'] = prefix

        env['FOR'] = self.fc
        if self.compiler.name == 'intel':
            env['FFLAGS'] = self.compiler.openmp_flag +" -mavx2 -mfma -O3 -ip -Ofast"
            env['LAPACK'] = "-qmkl=parallel -lmkl_scalapack_lp64 -lmkl_blacs_intelmpi_lp64"
        elif self.compiler.name == 'gcc':
            env['FFLAGS'] = self.compiler.openmp_flag +" -ffree-line-length-none -march=native -O3 -fcray-pointer -g3"
            env['LAPACK'] = "-lmkl_scalapack_lp64 -lmkl_blacs_openmpi_lp64 -lmkl_gf_lp64 -lmkl_gnu_thread -lmkl_core" # works with openmpi yet
        else:
            msg  = "The compiler you are building with, "
            msg += "'{0}', is not supported by sphng yet."
            raise InstallError(msg.format(self.compiler.name))

    def build(self, spec, prefix):

        make('goal')

    def install(self, spec, prefix):

        make('install')
