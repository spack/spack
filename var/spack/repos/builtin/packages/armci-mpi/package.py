# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install armci-mpi
#
# You can edit this file again by typing:
#
#     spack edit armci-mpi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class ArmciMpi(AutotoolsPackage):
    """ARMCI-MPI is an implementation of the ARMCI library used by Global Arrays.
       MPI-3 one-sided communication is used to implement ARMCI.
    """

    homepage = "https://github.com/pmodels/armci-mpi"
    url = "https://github.com/pmodels/armci-mpi/archive/refs/tags/v0.4.tar.gz"

    maintainers("jeffhammond")

    license("BSD-3-Clause", checked_by="jeffhammond")

    version("0.4", sha256="bcc3bb189b23bf653dcc69bc469eb86eae5ebc5ad94ab5f83e52ddbdbbebf1b1")
    version("0.3.1-beta", sha256="f3eaa8f365fb55123ecd9ced401086b0732e37e4df592b27916d71a67ab34fe9")

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("progress", default=False, description="Enable asynchronous progress")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi")

    def autoreconf(self, spec, prefix):
        # FIXME: Modify the autoreconf method as necessary
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = ["--enable-g"]

        shared = int(self.spec.variants["shared"].value)
        if shared:
            args.extend([
                "--enable-shared",
            ])

        progress = int(self.spec.variants["progress"].value)
        if progress:
            args.extend([
                "--with-progress",
            ])

        return args
