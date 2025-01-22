# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E3smScorpio(CMakePackage):
    """The SCORPIO (Software for Caching Output and Reads for Parallel I/O)
    library is used by all the model components in DOE's Energy Exascale Earth
    System Model (E3SM) for reading input data and writing model output"""

    homepage = "https://e3sm.org/scorpio-parallel-io-library/"
    url = "https://github.com/E3SM-Project/scorpio/archive/refs/tags/scorpio-v1.4.1.tar.gz"

    maintainers("xylar", "altheaden")
    version("1.6.7", sha256="ae7b0eb9d1d48331f3103a9b226855ad46916152ff569f25c6f82b17211008f3")
    version("1.6.6", sha256="19672bbe987e57c548161f11f0b7c267943969f2e60a9639181d3a040aedff53")
    version("1.6.5", sha256="b81af12f3cadec25898c9b102775f77457f3dd95b878ee6c7edaf6eb0b16d4fc")
    version("1.6.4", sha256="4739718c82f39fa8f9922280175dcdab56786193df8f6fb07f145df1274ed828")
    version("1.6.3", sha256="66350046fa22c8a06fffb8bf2a0fc48c66f05bf00da3a6ab83a0fad9c3c91da4")
    version("1.6.2", sha256="fa97e3255c6c558960356ef7726db7ce21072cd42fb4cc18a5e2d54ca8eb8d56")
    version("1.6.1", sha256="5e2a406cfa9e8e54622e1671bbebc6f364992fa3671d71d154666a274aa8c5a3")
    version("1.6.0", sha256="fcc18b7eaf0dae4fc83e17a7ca2fc695f476fa96539881e37406efbcb821947d")
    version("1.4.2", sha256="e41b2725b2389df48b91932224a0dfb8c8fe6e98c7a49e1dfd65f7d49f7ffa81")
    version("1.4.1", sha256="7cb4589410080d7e547ef17ddabe68f749e6af019c1d0e6ee9f11554f3ff6b1a")

    variant("timing", default=False, description="Enable timing")
    variant("mpi", default=True, description="Enable MPI")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("gptl", when="+timing")
    depends_on("mpi", when="+mpi")
    depends_on("parallel-netcdf", when="+mpi")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")

    def cmake_args(self):
        opts = []
        opts.append(self.define("NetCDF_C_PATH", self.spec["netcdf-c"].prefix))
        opts.append(self.define("NetCDF_Fortran_PATH", self.spec["netcdf-fortran"].prefix))

        if self.spec.satisfies("+timing"):
            opts.append(self.define("PIO_ENABLE_TIMING", "ON"))
            opts.append(self.define("GPTL_PATH", self.spec["gptl"].prefix))
        else:
            opts.append(self.define("PIO_ENABLE_TIMING", "OFF"))

        if self.spec.satisfies("+mpi"):
            opts.append(self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc))
            opts.append(self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx))
            opts.append(self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc))
            opts.append(self.define("WITH_PNETCDF", "ON"))
            opts.append(self.define("PNETCDF_PATH", self.spec["parallel-netcdf"].prefix))
        else:
            opts.append(self.define("WITH_PNETCDF", "OFF"))

        return opts

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("NetCDF_C_PATH", self.spec["netcdf-c"].prefix)
        env.set("NetCDF_Fortran_PATH", self.spec["netcdf-fortran"].prefix)
        if self.spec.satisfies("+mpi"):
            env.set("PNETCDF_PATH", self.spec["parallel-netcdf"].prefix)
