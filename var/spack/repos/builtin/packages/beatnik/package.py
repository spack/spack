# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Beatnik(CMakePackage):
    """Fluid interface model solver and benchmark to test global communication strategies based on Pandya and Shkoller's Z-Model formulation."""

    homepage = "https://github.com/CUP-ECS/beatnik"
    git = "https://github.com/CUP-ECS/beatnik.git"

    maintainers("patrickb314", "JAStewart28")

    # Add proper versions and checksums here. W
    # version("1.0", sha256="XXX")
    version("develop", branch="develop")
    version("main", branch="main")

    # Dependencies for all Beatnik versions
    depends_on("blt", type='build')
    depends_on("mpi")
    depends_on("kokkos @4:")
    depends_on("silo @4.11:")
    depends_on("cabana +cajita +heffte +silo +mpi")

    # Dependencies for specific versions/branches
    depends_on("cabana @0.5.0", when="@1.0")
    depends_on("cabana @0.5.0", when="@main")
    depends_on("cabana @master", when="@develop")

    # CMake specific build functions
    def cmake_args(self):
        args = []

        # Pull BLT from teh spack spec so we don't need the submodule
        args.append("-DBLT_SOURCE_DIR:PATH={0}".format(self.spec["blt"].prefix))

        return args
