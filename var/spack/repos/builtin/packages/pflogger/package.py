# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pflogger(CMakePackage):
    """A parallel Fortran logger (based on the design of the Python logger)"""

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger"
    url = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger/archive/refs/tags/v1.6.1.tar.gz"
    git = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger.git"

    maintainers("mathomp4", "tclune")

    version("develop", branch="develop")
    version("main", branch="main")

    version("1.9.2", sha256="783879eb1326a911f6e22c016e8530644ed0d315660405f2b43df42ba8670acc")
    version("1.9.1", sha256="918965f5a748a3a62e54751578f5935a820407b988b8455f7f25c266b5b7fe3c")
    version("1.9.0", sha256="aacd9b7e188bee3a54a4e681adde32e3bd95bb556cbbbd2c725c81aca5008003")
    version("1.8.0", sha256="28ce9ac8af374253b6dfd8f53f8fd271c787d432645ec9bc6a5a01601dc56e19")
    version("1.6.1", sha256="114a15daa7994ab7d4eea463c3a9b8fe7df3da7d07a0004b5c40cf155e374916")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    variant("mpi", default=False, description="Enable MPI")

    # pFlogger needs careful versioning to build
    depends_on("gftl@:1.5", when="@:1.6")
    depends_on("gftl-shared@:1.3", when="@:1.6")
    depends_on("yafyaml@1.0-beta5", when="@:1.6")

    depends_on("gftl@1.6:", when="@1.8:")
    depends_on("gftl-shared@1.4:", when="@1.8:")
    depends_on("yafyaml@1.0-beta8:", when="@1.8:")

    depends_on("gftl@1.8.1:", when="@1.9:")
    depends_on("gftl-shared@1.5:", when="@1.9:")
    depends_on("yafyaml@1.0.4:", when="@1.9:")

    depends_on("mpi", when="+mpi")

    depends_on("cmake@3.12:", type="build")

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("+mpi"):
            args.extend(["-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc])

        return args
