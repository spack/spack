# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install trove
#
# You can edit this file again by typing:
#
#     spack edit trove
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Trove(MakefilePackage):
    """trove benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-trove"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="update-makefile")
    # version("v1.0.0", tag="v1.0.0")

    depends_on("mpi")
    depends_on("intel-oneapi-mkl")

    parallel=False

    def edit(self, spec, prefix):

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env['PREFIX'] = prefix

        env['FOR'] = self.fc
        if self.compiler.name == 'intel':
            env['FFLAGS'] = self.compiler.openmp_flag +" -mavx2 -mfma -O3 -ip -Ofast"
        else:
            msg  = "The compiler you are building with, "
            msg += "'{0}', is not supported by sphng yet."
            raise InstallError(msg.format(self.compiler.name))
        env['LAPACK'] = "-mkl=parallel -lmkl_scalapack_lp64 -lmkl_blacs_intelmpi_lp64"

    def build(self, spec, prefix):

        make()

    def install(self, spec, prefix):

        make('install')
