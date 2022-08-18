# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallelio(CMakePackage):
    """The Parallel IO libraries (PIO) are high-level parallel I/O C and
    Fortran libraries for applications that need to do netCDF I/O from
    large numbers of processors on a HPC system."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url = "https://github.com/NCAR/ParallelIO/archive/pio2_5_8.tar.gz"

    maintainers = ["jedwards4b"]

    version("2_5_8", sha256="f2584fb4310ff7da39d51efbe3f334efd0ac53ae2995e5fc157decccc0570a89")
    version("2_5_7", sha256="af8af04e41af17f98f2c90b996ef0d8bcd980377e0b35e57b38938c7fdc87cbd")
    version("2_5_4", sha256="e51dc71683da808a714deddc1a80c2650ce847110383e42f1710f3ba567e7a65")
    version("2_5_2", sha256="935bc120ef3bf4fe09fb8bfdf788d05fb201a125d7346bf6b09e27ac3b5f345c")

    variant("pnetcdf", default=False, description="enable pnetcdf")
    variant("timing", default=False, description="enable GPTL timing")
    variant("logging", default=False, description="enable verbose logging")
    variant(
        "fortran", default=True, description="enable fortran interface (requires netcdf fortran)"
    )

    depends_on("mpi")
    depends_on("netcdf-c +mpi", type="link")
    depends_on("netcdf-fortran", type="link", when="+fortran")
    depends_on("parallel-netcdf", type="link", when="+pnetcdf")

    resource(name="genf90", git="https://github.com/PARALLELIO/genf90.git", tag="genf90_200608")

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        env["CC"] = spec["mpi"].mpicc
        env["FC"] = spec["mpi"].mpifc
        src = self.stage.source_path
        args = [
            define("NetCDF_C_PATH", spec["netcdf-c"].prefix),
            define("USER_CMAKE_MODULE_PATH", join_path(src, "cmake")),
            define("GENF90_PATH", join_path(src, "genf90")),
        ]
        if spec.satisfies("+pnetcdf"):
            args.extend(
                [
                    define("PnetCDF_C_PATH", spec["parallel-netcdf"].prefix),
                ]
            )
        if spec.satisfies("+fortran"):
            args.extend(
                [
                    define("NetCDF_Fortran_PATH", spec["netcdf-fortran"].prefix),
                ]
            )

        args.extend(
            [
                define_from_variant("PIO_ENABLE_TIMING", "timing"),
                define_from_variant("PIO_ENABLE_LOGGING", "logging"),
                define_from_variant("PIO_ENABLE_FORTRAN", "fortran"),
            ]
        )
        return args
