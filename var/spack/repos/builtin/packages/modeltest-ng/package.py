# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModeltestNg(CMakePackage):
    """Best-fit model selection"""

    homepage = "https://github.com/ddarriba/modeltest"
    url = "https://github.com/ddarriba/modeltest/archive/refs/tags/v0.1.7.tar.gz"
    git = "https://github.com/ddarriba/modeltest.git"

    maintainers("dorton21")

    version("0.1.7", commit="cc028888f1d4222aaa53b99c6b02cd934a279001", submodules=True)

    variant("mpi", default=False, description="Enable MPI")

    depends_on("glib")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("openmpi", when="+mpi")

    def cmake_args(self):
        return [self.define_from_variant("ENABLE_MPI", "mpi")]
