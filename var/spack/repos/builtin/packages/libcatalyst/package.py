# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcatalyst(CMakePackage):
    """Catalyst is an API specification developed for simulations (and other
    scientific data producers) to analyze and visualize data in situ."""

    homepage = "https://gitlab.kitware.com/paraview/catalyst"
    git = "https://gitlab.kitware.com/paraview/catalyst.git"
    url = "https://gitlab.kitware.com/api/v4/projects/paraview%2Fcatalyst/packages/generic/catalyst/v2.0.0/catalyst-v2.0.0.tar.gz"

    maintainers("mathstuf")

    version("2.0.0-rc3", sha256="8862bd0a4d0be2176b4272f9affda1ea4e5092087acbb99a2fe2621c33834e05")

    # master as of 2021-05-12
    version("0.20210512", commit="8456ccd6015142b5a7705f79471361d4f5644fa7")

    variant("mpi", default=False, description="Enable MPI support")

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
