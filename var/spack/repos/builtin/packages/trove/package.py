# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
