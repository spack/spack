# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MpiSerial(AutotoolsPackage):
    """A single processor implementation of the mpi library."""

    homepage = "https://github.com/MCSclimate/mpi-serial"
    url = "https://github.com/MCSclimate/mpi-serial/archive/refs/tags/MPIserial_2.3.0.tar.gz"

    # notify when the package is updated.
    maintainers("jedwards4b")

    version("2.3.0", sha256="cc55e6bf0ae5e1d93aafa31ba91bfc13e896642a511c3101695ea05eccf97988")

    variant(
        "fort-real-size",
        values=int,
        default=4,
        description="Specify the size of Fortran real variables",
    )

    variant(
        "fort-double-size",
        values=int,
        default=8,
        description="Specify the size of Fortran double precision variables",
    )

    patch("install.patch")

    provides("mpi")

    def configure_args(self):
        args = ["CFLAGS={0}".format(self.compiler.cc_pic_flag)]
        realsize = int(self.spec.variants["fort-real-size"].value)
        if realsize != 4:
            args.extend(["--enable-fort-real={0}".format(realsize)])
        doublesize = int(self.spec.variants["fort-double-size"].value)
        if doublesize != 8:
            args.extend(["--enable-fort-double={0}".format(doublesize)])
        return args
