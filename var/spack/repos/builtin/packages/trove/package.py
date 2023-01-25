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
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/UniOfLeicester/benchmark-trove"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", tag="v1.0.0")

    variant("mpi", default=True, description="Enable MPI support")
    depends_on("intel-oneapi-mpi", when="+mpi")
    depends_on("intel-oneapi-mkl")

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def build(self, spec, prefix):
        if "+mpi" in spec:
            fc = spec["mpi"].mpifc
        else:
            fc = os.environ["FC"]

        make(f'FOR={fc}')

    def install(self, spec, prefix):

        make('install','PREFIX='+prefix+'/bin')
