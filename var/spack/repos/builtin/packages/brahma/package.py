# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brahma(CMakePackage):
    """Interceptor library for I/O calls using Gotcha"""

    homepage = "https://github.com/hariharan-devarajan/brahma"
    git = "https://github.com/hariharan-devarajan/brahma.git"
    maintainers("hariharan-devarajan")

    version("develop", branch="dev")
    version("master", branch="master")
    version("0.0.1", tag="v0.0.1", commit="15156036f14e36511dfc3f3751dc953540526a2b")

    variant("mpi", default=False, description="Enable MPI support")
    depends_on("cpp-logger@0.0.1")
    depends_on("gotcha@develop")
    depends_on("catch2@3.0.1")

    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        return [self.define_from_variant("BUILD_WITH_MPI", "mpi")]
