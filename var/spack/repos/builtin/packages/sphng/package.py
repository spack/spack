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
#     spack install sphng
#
# You can edit this file again by typing:
#
#     spack edit sphng
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Sphng(MakefilePackage):
    """sphNG benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-sphng"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-sphng.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", tag="v1.0.0")

    variant("mpi", default=True, description="Enable MPI support")

    executables = [r"^sph_tree_rk_gradh$"]

    depends_on("intel-oneapi-mpi", when="+mpi")
    depends_on("intel-oneapi-compilers")

    # if "+mpi" in spec:
    #     fc = spec["mpi"].mpifc
    # else:
    #     fc = os.environ["FC"]

    parallel=False

    def edit(self, spec, prefix):

        self.cc = spack_cc if "~mpi" in spec else spec["mpi"].mpicc
        self.cxx = spack_cxx if "~mpi" in spec else spec["mpi"].mpicxx
        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

    def build(self, spec, prefix):

        make('mpi=yes openmp=yes gradhrk', f'FC={self.fc}', 'SYSTEM=dirac3-intel19')

    def install(self, spec, prefix):

        make('install', f'PREFIX={prefix}', f'FC={self.fc}', 'SYSTEM=dirac3-intel19')
