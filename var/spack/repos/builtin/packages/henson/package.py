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
    depends_on("py-mpi4py", type=("build", "run"), when="+python")
    variant("mpi-wrappers", default=False, description="Build MPI wrappers (PMPI)")

    variant("boost", default=False, description="Use Boost for coroutine support")
    depends_on("boost+context", type=("build", "run"), when="+boost")
    conflicts("~boost", when="target=aarch64:")

    conflicts("^openmpi", when="+mpi-wrappers")

    def cmake_args(self):
        args = [
            self.define_from_variant("python", "python"),
            self.define_from_variant("mpi-wrappers", "mpi-wrappers"),
            self.define_from_variant("use_boost", "boost"),
        ]

        if self.spec.satisfies("+python"):
            args += [self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path)]

        return args
