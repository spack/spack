# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PrunersNinja(AutotoolsPackage):
    """NINJA: Noise Inject agent tool to expose subtle and unintended message
       races."""
    homepage = "https://github.com/PRUNERS/NINJA"
    url      = "https://github.com/PRUNERS/NINJA/releases/download/v1.0.0/NINJA-1.0.0.tar.gz"

    version("1.0.1", "f0728cad61d8f1f970dffb7bb430addb")
    version("1.0.0", "fee53c4712ac521ebec3cd8692e5185a")

    depends_on("mpi")
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
