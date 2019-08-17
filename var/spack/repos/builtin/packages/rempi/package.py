# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rempi(AutotoolsPackage):
    """ReMPI is a record-and-replay tool for MPI applications."""
    homepage = "https://github.com/PRUNERS/ReMPI"
    url      = "https://github.com/PRUNERS/ReMPI/releases/download/v1.0.0/ReMPI-1.0.0.tar.gz"

    version("1.1.0", "05b872a6f3e2f49a2fc6112a844c7f43")
    version("1.0.0", "32c780a6a74627b5796bea161d4c4733")

    depends_on("mpi")
    depends_on("zlib")
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
