# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsWeatherModel(CMakePackage):
    """The Unified Forecast System (UFS) Weather Model (WM) is a prognostic
    model that can be used for short- and medium-range research and
    operational forecasts, as exemplified by its use in the operational Global
    Forecast System (GFS) of the National Oceanic and Atmospheric
    Administration (NOAA)."""

    homepage = "https://ufs-weather-model.readthedocs.io/en/latest/"
    url = "https://github.com/ufs-community/ufs-weather-model/archive/refs/tags/ufs-v1.1.0.tar.gz"
    git = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers("t-brown")

    version("2.0.0", tag="ufs-v2.0.0", submodules=True)
    version("1.1.0", tag="ufs-v1.1.0", submodules=True)

    variant(
        "32bit", default=True, description="Enable 32-bit single precision arithmetic in dycore"
    )
    variant("avx2", default=False, description="Enable AVX2 instructions")
    variant(
        "ccpp", default=True, description="Enable the Common Community Physics Package (CCPP))"
    )
    variant(
        "ccpp_suites",
        default="FV3_GFS_v15p2,FV3_RRFS_v1alpha",
        description="CCPP suites to compile",
        values=("FV3_GFS_v15p2", "FV3_RRFS_v1alpha", "FV3_GFS_v15p2,FV3_RRFS_v1alpha"),
        multi=True,
    )
    variant("inline_post", default=False, description="Compile post processing inline")
    variant("multi_gases", default=False, description="Enable multi gases in physics routines")
    variant("openmp", default=True, description="Enable OpenMP")
    variant("parallel_netcdf", default=True, description="Enable parallel I/O in netCDF")
    variant(
        "quad_precision",
        default=False,
        description="Enable quad precision for certain grid metric terms in dycore",
    )
    variant(
        "simdmultiarch", default=False, description="Enable multi-target SIMD instruction sets"
    )

    depends_on("bacio")
    depends_on("esmf@:8.0.0")
    depends_on("mpi")
    depends_on("nemsio")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("w3nco")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CMAKE_C_COMPILER", spec["mpi"].mpicc)
        env.set("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx)
        env.set("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc)
        env.set("ESMFMKFILE", join_path(spec["esmf"].prefix.lib, "esmf.mk"))

        env.set("CCPP_SUITES", ",".join([x for x in spec.variants["ccpp_suites"].value if x]))

        if spec.platform == "linux" and spec.satisfies("%intel"):
            env.set("CMAKE_Platform", "linux.intel")
        elif spec.platform == "linux" and spec.satisfies("%gcc"):
            env.set("CMAKE_Platform", "linux.gnu")
        elif spec.platform == "darwin" and spec.satisfies("%gcc"):
            env.set("CMAKE_Platform", "macosx.gnu")
        else:
            msg = "The host system {0} and compiler {0} "
            msg += "are not supported by UFS."
            raise InstallError(msg.format(spec.platform, self.compiler.name))

    def cmake_args(self):
        from_variant = self.define_from_variant
        args = [
            from_variant("32BIT", "32bit"),
            from_variant("AVX2", "avx2"),
            from_variant("CCPP", "ccpp"),
            from_variant("INLINE_POST", "inline_post"),
            from_variant("MULTI_GASES", "multi_gases"),
            from_variant("OPENMP", "openmp"),
            from_variant("PARALLEL_NETCDF", "parallel_netcdf"),
            from_variant("QUAD_PRECISION", "quad_precision"),
            from_variant("SIMDMULTIARCH", "simdmultiarch"),
        ]

        return args

    @run_after("install")
    def install_additional_files(self):
        mkdirp(prefix.bin)
        ufs_src = join_path(self.build_directory, "NEMS.exe")
        ufs_dst = join_path(prefix.bin, "ufs_weather_model")
        install(ufs_src, ufs_dst)
        set_executable(ufs_dst)
