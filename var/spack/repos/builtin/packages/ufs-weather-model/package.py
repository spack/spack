# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

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

    maintainers = ["t-brown", "AlexanderRichert-NOAA"]

    version("develop", branch="develop", submodules=True, commit="ea0b6e4")
    version("2.0.0", tag="ufs-v2.0.0", submodules=True)
    version("1.1.0", tag="ufs-v1.1.0", submodules=True)

    variant("mpi", default=True, description="Enable MPI")
    variant(
        "32bit", default=True, description="Enable 32-bit single precision arithmetic in dycore"
    )
    variant(
        "ccpp_32bit",
        default=False,
        description="Enable CCPP_32BIT (single precision arithmetic in slow physics)",
    )
    variant("avx2", default=True, description="Enable AVX2 instruction set")
    variant(
        "simdmultiarch", default=False, description="Enable multi-target SIMD instruction sets"
    )
    variant("debug", default=False, description="Enable DEBUG mode", when="@develop")
    variant(
        "debug_linkmpi",
        default=True,
        description="Enable linkmpi option when DEBUG mode is on",
        when="@develop",
    )
    variant("inline_post", default=False, description="Enable inline post")
    variant("multi_gases", default=False, description="Enable multi gases in physics routines")
    variant("moving_nest", default=False, description="Enable moving nest code", when="@develop")
    variant("openmp", default=True, description="Enable OpenMP")
    variant("parallel_netcdf", default=True, description="Enable parallel NetCDF")
    variant(
        "jedi_driver",
        default=False,
        description="Enable JEDI as top level driver",
        when="@develop",
    )
    variant(
        "cmeps_aoflux",
        default=False,
        description="Enable atmosphere-ocean flux calculation in mediator",
        when="@develop",
    )
    variant(
        "ccpp",
        default=True,
        description="Enable the Common Community Physics Package (CCPP)",
        when="@:2.0.0",
    )
    variant(
        "ccpp_suites",
        default="FV3_GFS_v15p2,FV3_RRFS_v1alpha",
        description="CCPP suites to compile",
        values=("FV3_GFS_v15p2", "FV3_RRFS_v1alpha", "FV3_GFS_v15p2,FV3_RRFS_v1alpha"),
        multi=True,
        when="@:2.0.0",
    )
    dev_ccpp_default = [
        "FV3_GFS_v16",
        "FV3_GFS_v15_thompson_mynn",
        "FV3_GFS_v17_p8",
        "FV3_GFS_v17_p8_rrtmgp",
        "FV3_GFS_v15_thompson_mynn_lam3km",
    ]
    variant(
        "ccpp_suites",
        default=",".join(dev_ccpp_default),
        description="CCPP suites to compile",
        multi=True,
        when="@develop",
    )
    variant(
        "quad_precision",
        default=False,
        description="Enable quad precision for certain grid metric terms in dycore",
        when="@:2.0.0",
    )
    variant("mom6solo", default=False, description="Build MOM6 solo executable", when="@develop")

    variant("cmake_platform", default="auto", description="Override value for CMAKE_Platform env variable ('linux.intel', 'hera.gnu', 'acorn', etc.)")

    variant("app", default="ATM", description="UFS application", when="@develop")

    depends_on("bacio")
    depends_on("mpi", when="+mpi")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("esmf@:8.0.0", when="@:2.0.0")
    depends_on("nemsio", when="@:2.0.0")
    depends_on("w3nco", when="@:2.0.0")
    depends_on("crtm", when="@develop")
    depends_on("esmf", when="@develop")
    depends_on("esmf+debug", when="+debug")
    depends_on("fms", when="@develop")
    depends_on("fms constants=GFS", when="@develop ^fms@2022.02:")
    depends_on("g2", when="@develop")
    depends_on("g2tmpl", when="@develop")
    depends_on("hdf5+hl+mpi", when="@develop")
    depends_on("ip", when="@develop")
    depends_on("netcdf-c~parallel-netcdf+mpi", when="@develop")
    depends_on("parallelio+fortran~pnetcdf~shared", when="@develop")
    with when("@develop app=S2SA"):
        depends_on("mapl")
        depends_on("gftl-shared")
    with when("@develop app=S2SWA"):
        depends_on("mapl")
        depends_on("gftl-shared")
    with when("@develop app=ATMAERO"):
        depends_on("mapl")
        depends_on("gftl-shared")
    depends_on("mapl+debug", when="+debug ^mapl")

    conflicts("%gcc:8", when="@develop")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CC", spec["mpi"].mpicc)
        env.set("CXX", spec["mpi"].mpicxx)
        env.set("FC", spec["mpi"].mpifc)

        env.set("CCPP_SUITES", ",".join([x for x in spec.variants["ccpp_suites"].value if x]))

        if spec.variants["cmake_platform"].value != "auto":
            env.set("CMAKE_Platform", spec.variants["cmake_platform"].value)
        elif spec.platform == "linux" and spec.satisfies("%intel"):
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
            from_variant("CCPP_32BIT", "ccpp_32bit"),
            from_variant("AVX2", "avx2"),
            from_variant("SIMDMULTIARCH", "simdmultiarch"),
            from_variant("DEBUG", "debug"),
            from_variant("DEBUG_LINKMPI", "debug_linkmpi"),
            from_variant("INLINE_POST", "inline_post"),
            from_variant("MULTI_GASES", "multi_gases"),
            from_variant("MOVING_NEST", "moving_nest"),
            from_variant("OPENMP", "openmp"),
            from_variant("PARALLEL_NETCDF", "parallel_netcdf"),
            from_variant("JEDI_DRIVER", "jedi_driver"),
            from_variant("CMEPS_AOFLUX", "cmeps_aoflux"),
            from_variant("APP", "app"),
            from_variant("CCPP_SUITES", "ccpp_suites").replace(";", ","),
            from_variant("MPI", "mpi"),
        ]
        if self.spec.satisfies("@:2.0.0"):
            args.append(from_variant("CCPP", "ccpp"))
            args.append(from_variant("QUAD_PRECISION", "quad_precision"))

        return args

    def patch(self):
        # Modify hardcoded version numbers in CMakeLists.txt:
        pkgs = {
            "bacio": "bacio",
            "esmf": "ESMF",
            "fms": "FMS",
            "netcdf-c": "NetCDF",
            "parallelio": "PIO",
            "sp": "sp",
            "w3emc": "w3emc",
        }

        for pkg in pkgs.keys():
            filter_file(
                r"(find_package\(\s*%s)\s+[\d\.]+" % pkgs[pkg],
                r"\1 " + re.sub(r"(\d+\.\d+\.\d+).+", r"\1", str(self.spec[pkg].version)),
                "CMakeLists.txt",
            )

        # Fix ESMF capitalization/-lEMSF issue when using GOCART:
        if self.spec.satisfies("@develop") and any(
            ["app=" + app in self.spec for app in ["S2SA", "S2SWA", "ATMAERO"]]
        ):
            filter_file(r"NOT TARGET esmf", r"NOT TARGET ESMF", "WW3/model/src/CMakeLists.txt")
            filter_file(r"PUBLIC esmf\)", "PUBLIC ESMF)", "WW3/model/src/CMakeLists.txt")
            filter_file(r"\(esmf ", r"(ESMF ", "CMakeModules/Modules/FindESMF.cmake")

    @run_after("install")
    def install_additional_files(self):
        mkdirp(prefix.bin)
        if self.spec.satisfies("@develop"):
            ufs_src = join_path(self.build_directory, "ufs_model")
        else:
            ufs_src = join_path(self.build_directory, "NEMS.exe")
        ufs_dst = join_path(prefix.bin, "ufs_weather_model")
        install(ufs_src, ufs_dst)
        set_executable(ufs_dst)
