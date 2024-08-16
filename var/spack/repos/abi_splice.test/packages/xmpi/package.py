# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmpi(Package):
    homepage = "https://www.example.com"
    has_code = False
    provides("mpi")
    variant("abi", default="custom", multi=False, values=("mpich", "openmpi", "custom"))
    version("6.0")
    provides("mpi@1", when="@6.0")
    can_splice("mpich@1.0", when="@6.0 abi=mpich")
    can_splice("openmpi@1.0", when="@6.0 abi=openmpi")
    version("7.0")
    provides("mpi@2", when="@7.0")
    can_splice("mpich@2.0", when="@7.0 abi=mpich")
    can_splice("openmpi@2.0", when="@7.0 abi=openmpi")
    version("8.0")
    provides("mpi@3", when="@8.0")
    can_splice("mpich@3.0", when="@8.0 abi=mpich")
    can_splice("openmpi@3.0", when="@8.0 abi=openmpi")

    def install(self, spec, prefix):
        touch(prefix.foo)
