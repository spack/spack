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

    variant("timing", default=False, description="Enable GPTL timing")
    variant("mpi", default=True, description="Enable MPI")
    variant("internal-timing", default=False,
            description="Gather and print GPL timing stats")
    variant("tools", default=False, description="Enable SCORPIO tools")
    variant("malloc", default=True,
            description="Use native malloc (instead of bget package)")

    depends_on("gptl", when="+timing")
    depends_on("mpi", when="+mpi")
    depends_on("parallel-netcdf", type="link", when="+mpi")
    depends_on("netcdf-c", type="link")
    depends_on("netcdf-fortran", type="link")

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        args = [
            define("NetCDF_C_PATH", spec["netcdf-c"].prefix),
            define("NetCDF_Fortran_PATH", spec["netcdf-fortran"].prefix),
        ]

        if self.spec.satisfies("+timing"):
            args.append(define("GPTL_PATH", spec["gptl"].prefix))

        if spec.satisfies("+mpi"):
            args.append(define("CMAKE_C_COMPILER", spec["mpi"].mpicc))
            args.append(define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx))
            args.append(define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))
            args.extend([
                define("PnetCDF_C_PATH", spec["parallel-netcdf"].prefix),
                define("PnetCDF_Fortran_PATH", spec["parallel-netcdf"].prefix),
            ])

        args.extend([
            define_from_variant("WITH_PNETCDF", "mpi"),
            define_from_variant("PIO_ENABLE_TIMING", "timing"),
            define_from_variant("PIO_ENABLE_INTERNAL_TIMING",
                                "internal-timing"),
            define_from_variant("PIO_ENABLE_TOOLS", "tools"),
            define_from_variant("PIO_USE_MALLOC", "malloc"),
        ])

        return args
