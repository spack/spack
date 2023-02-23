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
#     spack install trove-pdsyev
#
# You can edit this file again by typing:
#
#     spack edit trove-pdsyev
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class TrovePdsyev(MakefilePackage):
    """trove-pdsyev benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-trove-pdsyev"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-trove-pdsyev.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", branch="main")
    # version("v1.0.0", tag="v1.0.0")

    executables = [r"^diag_generic.x$"]

    # depends_on("mpi")
    # depends_on("mkl")
    # depends_on("scalapack")
    depends_on("ipp")

    parallel=False

    def edit(self, spec, prefix):

        if self.compiler.name != 'intel':
            msg  = "Only intel is supported"
            msg += "'{0}', is not supported by trove-pdsyev yet."
            raise InstallError(msg.format(self.compiler.name))

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env['DESTDIR'] = ''
        env['PREFIX'] = prefix
        env['FC'] = self.fc

        makefile = FileFilter("Makefile")
        makefile.filter(r'PLAT\s*=.*', 'PLAT = _generic')
        makefile.filter(r'FOR\s*= .*', 'ifort')

        if "~ipp" in spec:
            makefile.filter(r'(.*)-use-intel-optimized-headers(.*)', r'\1 \2')

    def build(self, spec, prefix):

        make('')

    def install(self, spec, prefix):

        make('install')
