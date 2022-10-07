# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcatalyst(CMakePackage):
    """Catalyst is an API specification developed for simulations (and other
    scientific data producers) to analyze and visualize data in situ."""

    homepage = "https://gitlab.kitware.com/paraview/catalyst"
    git = "https://gitlab.kitware.com/paraview/catalyst.git"

    maintainers = ["mathstuf"]

    # master as of 2021-05-12
    version("2021-05-12", commit="8456ccd6015142b5a7705f79471361d4f5644fa7")

    variant("mpi", default=False, description="Enable MPI support")
    variant("python3", default=False, description="Enable Python3 support")

    depends_on("mpi", when="+mpi")

    # TODO: catalyst doesn't support an external conduit
    # depends_on('conduit')

    def cmake_args(self):
        """Populate cmake arguments for libcatalyst."""
        args = [
            "-DCATALYST_BUILD_TESTING=OFF",
            self.define_from_variant("CATALYST_USE_MPI", "mpi"),
        ]

        return args
