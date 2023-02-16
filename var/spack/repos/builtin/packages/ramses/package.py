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
#     spack install ramses
#
# You can edit this file again by typing:
#
#     spack edit ramses
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Ramses(MakefilePackage):
    """Ramses benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-ramses"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-ramses.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="update-makefile")
    # version("v1.0.0", tag="v1.0.0")

    executables = [r"^ramses3d$"]

    depends_on("mpi")

    parallel=False

    def edit(self, spec, prefix):

        env['PREFIX'] = prefix
        env['F90'] = spack_fc if "~mpi" in spec else spec["mpi"].mpifc
        if self.compiler.name == 'intel':
            env['FFLAGS'] = "-O3 -cpp -fpe0 -ftrapuv -ipo -DNOSYSTEM"
        elif self.compiler.name == 'gcc':
            if 'mpiifort' in spec["mpi"].mpifc:
                env['F90'] = "mpif90".join(spec["mpi"].mpifc.rsplit('mpiifort', 1))
            env['FFLAGS'] = "-O3 -cpp -march=core-avx2 -fomit-frame-pointer -ffree-line-length-none"
            # env['OLD_MPI_SUPPORT'] = "1"
        else:
            msg  = "The compiler you are building with, "
            msg += "'{0}', is not supported by ramses yet."
            raise InstallError(msg.format(self.compiler.name))

    def build(self, spec, prefix):

        os.chdir(os.path.join(os.getcwd(),'SRC','bin'))
        make()

    def install(self, spec, prefix):

        make('install')
