# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Henson(CMakePackage):
    """Cooperative multitasking for in situ processing."""

    homepage = "https://github.com/henson-insitu/henson"
    git = "https://github.com/henson-insitu/henson.git"

    version("master", branch="master")

    maintainers("mrzv")

    depends_on("mpi")

    variant("python", default=False, description="Build Python bindings")
    extends("python", when="+python")
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    variant("mpi-wrappers", default=False, description="Build MPI wrappers (PMPI)")

    conflicts("^openmpi", when="+mpi-wrappers")

    def cmake_args(self):
        args = [
            self.define_from_variant("python", "python"),
            self.define_from_variant("mpi-wrappers", "mpi-wrappers"),
        ]

        if self.spec.satisfies("+python"):
            args += [self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path)]

        return args
