# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *

#
# Need to add:
#  KOKKOS support using an external (i.e. spack-supplied) kokkos library.
#  Data Warehouse (FAODEL) enable/disable


class Seacas(CMakePackage):
    """The SEACAS Project contains the Exodus and IOSS I/O libraries
    and a collection of applications which create, query, modify, or
    translate Exodus databases.  Exodus is a finite element mesh and
    results database file format.

    Default is to build the Exodus and IOSS libraries and the
    io_shell, io_info, io_modify, struc_to_unstruc apps.
    """

    homepage = "https://sandialabs.github.io/seacas/"
    git = "https://github.com/sandialabs/seacas.git"
    url = "https://github.com/sandialabs/seacas/archive/v2019-08-20.tar.gz"
    maintainers("gsjaardema")

    # ###################### Versions ##########################
    version("master", branch="master")
    version(
        "2023-10-24", sha256="f93bf0327329c302ed3feb6adf2e3968f01ec325084a457b2c2dbbf6c4f751a2"
    )
    version(
        "2023-05-30", sha256="3dd982841854466820a3902163ad1cf1b3fbab65ed7542456d328f2d1a5373c1"
    )
    version(
        "2022-10-14", sha256="cde91e7561d2352045d669a25bdf46a604d85ed1ea7f3f5028004455e4ce9d56"
    )
    version(
        "2022-05-16", sha256="22ff67045d730a2c7d5394c9034e44a2033cc82a461574f93d899e9aa713d4ae"
    )
    version(
        "2022-03-04", sha256="a934a473e1fdfbc8dbb55058358551a02e03a60e5cdbf2b28b8ecd3d9500bfa5"
    )
    version(
        "2022-02-16", sha256="a6accb9924f0f357f63a01485c3eaaf5ceb6a22dfda73fc9bfb17d7e2f565098"
    )
    version(
        "2022-01-27", sha256="beff12583814dcaf75cf8f1a78bb183c1dcc8937bc18d5206672e3a692db05e0"
    )
    version(
        "2021-10-11", sha256="f8a6dac813c0937fed4a5377123aa61d47eb459ba87ddf368d02ebe10c2c3a0d"
    )
    version(
        "2021-09-30", sha256="5d061e35e93eb81214da3b67ddda2829cf5efed38a566be6363a9866ba2f9ab3"
    )
    version(
        "2021-05-12", sha256="92663767f0317018d6f6e422e8c687e49f6f7eb2b92e49e837eb7dc0ca0ac33d"
    )
    version(
        "2021-04-05", sha256="76f66eec1fec7aba30092c94c7609495e6b90d9dcb6f35b3ee188304d02c6e04"
    )
    version(
        "2021-01-20", sha256="7814e81981d03009b6816be3eb4ed3845fd02cc69e006ee008a2cbc85d508246"
    )
    version(
        "2021-01-06", sha256="b233502a7dc3e5ab69466054cf358eb033e593b8679c6721bf630b03999bd7e5"
    )
    version(
        "2020-08-13", sha256="e5eaf203eb2dbfb33c61ccde26deea459d058aaea79b0847e2f4bdb0cef1ddcb"
    )
    version(
        "2020-05-12", sha256="7fc6915f60568b36e052ba07a77d691c99abe42eaba6ae8a6dc74bb33490ed60"
    )
    version(
        "2020-03-16", sha256="2eb404f3dcb17c3e7eacf66978372830d40ef3722788207741fcd48417807af6"
    )
    version(
        "2020-01-16", sha256="5ae84f61e410a4f3f19153737e0ac0493b144f20feb1bbfe2024f76613d8bff5"
    )
    version(
        "2019-12-18", sha256="f82cfa276ebc5fe6054852383da16eba7a51c81e6640c73b5f01fc3109487c6f"
    )
    version(
        "2019-10-14", sha256="ca4cf585cdbc15c25f302140fe1f61ee1a30d72921e032b9a854492b6c61fb91"
    )
    version(
        "2019-08-20", sha256="a82c1910c2b37427616dc3716ca0b3c1c77410db6723aefb5bea9f47429666e5"
    )
    version(
        "2019-07-26", sha256="651dac832b0cfee0f63527f563415c8a65b8e4d79242735c1e2aec606f6b2e17"
    )

    # ###################### Variants ##########################
    # Package options
    # The I/O libraries (exodus, IOSS) are always built
    # -- required of both applications and legacy variants.
    variant(
        "applications",
        default=True,
        description='Build all "current" SEACAS applications. This'
        " includes a debatable list of essential applications: "
        "aprepro, conjoin, cpup, ejoin, epu, exo2mat, mat2exo, "
        "exo_format, exodiff, explore, grepos, io_shell, io_info, "
        "io_modify, nemslice, nemspread, zellij",
    )
    variant(
        "legacy",
        default=True,
        description='Build all "legacy" SEACAS applications. This includes'
        ' a debatable list of "legacy" applications: algebra, blot, '
        "exomatlab, exotxt, fastq, gen3d, genshell, gjoin, mapvar, "
        "mapvar-kd, numbers, txtexo, nemesis",
    )

    # Build options
    variant("fortran", default=True, description="Compile with Fortran support")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="Enables MPI parallelism.")

    variant(
        "thread_safe", default=False, description="Enable thread-safe exodus and IOSS libraries"
    )

    # TPLs (alphabet order)
    variant("adios2", default=False, description="Enable ADIOS2")
    variant("cgns", default=True, description="Enable CGNS")
    variant("faodel", default=False, description="Enable Faodel")
    variant("matio", default=True, description="Compile with matio (MatLab) support")
    variant("metis", default=False, description="Compile with METIS and ParMETIS")
    variant("x11", default=True, description="Compile with X11")

    # ###################### Dependencies ##########################
    depends_on("cmake@3.22:", when="@2023-10-24:", type="build")
    depends_on("cmake@3.17:", when="@:2023-05-30", type="build")
    depends_on("mpi", when="+mpi")

    # Always depends on netcdf-c
    depends_on("netcdf-c@4.8.0:+mpi+parallel-netcdf", when="+mpi")
    depends_on("netcdf-c@4.8.0:~mpi", when="~mpi")
    depends_on("hdf5+hl~mpi", when="~mpi")

    depends_on("fmt@10.1.0", when="@2023-10-24:")
    depends_on("fmt@9.1.0", when="@2022-10-14:2023-05-30")
    depends_on("fmt@8.1.0:9", when="@2022-03-04:2022-05-16")

    depends_on("matio", when="+matio")
    depends_on("libx11", when="+x11")

    with when("+cgns"):
        depends_on("cgns@4.2.0:+mpi+scoping", when="+mpi")
        depends_on("cgns@4.2.0:~mpi+scoping", when="~mpi")

    with when("+adios2"):
        depends_on("adios2@master")
        depends_on("adios2~mpi", when="~mpi")
        depends_on("adios2+mpi", when="+mpi")

    with when("+metis"):
        depends_on("metis+int64+real64")
        depends_on("parmetis+int64", when="+mpi")

    # The Faodel TPL is only supported in seacas@2021-04-05:
    depends_on("faodel@1.2108.1:+mpi", when="+faodel +mpi")
    depends_on("faodel@1.2108.1:~mpi", when="+faodel ~mpi")
    conflicts(
        "+faodel",
        when="@:2021-01-20",
        msg="The Faodel TPL is only compatible with @2021-04-05 and later.",
    )

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant
        define = self.define

        if self.spec.satisfies("@2022-10-14:"):
            project_name_base = "Seacas"
        else:
            project_name_base = "SEACASProj"

        options = []

        # #################### Base Settings #######################

        options.extend(
            [
                define(project_name_base + "_ENABLE_TESTS", True),
                define(project_name_base + "_ENABLE_CXX11", True),
                define(project_name_base + "_ENABLE_Kokkos", False),
                define(project_name_base + "_HIDE_DEPRECATED_CODE", False),
                from_variant("CMAKE_INSTALL_RPATH_USE_LINK_PATH", "shared"),
                from_variant("BUILD_SHARED_LIBS", "shared"),
                from_variant("SEACASExodus_ENABLE_THREADSAFE", "thread_safe"),
                from_variant("SEACASIoss_ENABLE_THREADSAFE", "thread_safe"),
                # SEACASExodus_ENABLE_THREADSAFE=ON requires TPL_ENABLE_Pthread=ON
                from_variant("TPL_ENABLE_Pthread", "thread_safe"),
                from_variant("TPL_ENABLE_X11", "x11"),
                from_variant(project_name_base + "_ENABLE_Fortran", "fortran"),
            ]
        )

        options.append(from_variant("TPL_ENABLE_MPI", "mpi"))
        if "+mpi" in spec:
            options.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    define("MPI_BASE_DIR", spec["mpi"].prefix),
                ]
            )

        # ########## What applications should be built #############
        # Check whether they want everything; if so, do the easy way...
        if "+applications" in spec and "+legacy" in spec:
            options.extend(
                [
                    define(project_name_base + "_ENABLE_ALL_PACKAGES", True),
                    define(project_name_base + "_ENABLE_ALL_OPTIONAL_PACKAGES", True),
                    define(project_name_base + "_ENABLE_SECONDARY_TESTED_CODE", True),
                ]
            )

        else:
            # Don't want everything; handle the subsets:
            options.extend(
                [
                    define(project_name_base + "_ENABLE_ALL_PACKAGES", False),
                    define(project_name_base + "_ENABLE_ALL_OPTIONAL_PACKAGES", False),
                    define(project_name_base + "_ENABLE_SECONDARY_TESTED_CODE", False),
                    define(project_name_base + "_ENABLE_SEACASIoss", True),
                    define(project_name_base + "_ENABLE_SEACASExodus", True),
                    from_variant(project_name_base + "_ENABLE_SEACASExodus_for", "fortran"),
                    from_variant(project_name_base + "_ENABLE_SEACASExoIIv2for32", "fortran"),
                ]
            )

            if "+applications" in spec:
                # C / C++ applications
                for app in (
                    "Aprepro",
                    "Aprepro_lib",
                    "Conjoin",
                    "Cpup",
                    "Ejoin",
                    "Epu",
                    "Exo2mat",
                    "Exo_format",
                    "Exodiff",
                    "Mat2exo",
                    "Nas2exo",
                    "Nemslice",
                    "Nemspread",
                    "Slice",
                    "Zellij",
                ):
                    options.append(define(project_name_base + "_ENABLE_SEACAS" + app, True))
                # Fortran-based applications
                for app in ("Explore", "Grepos"):
                    options.append(
                        from_variant(project_name_base + "_ENABLE_SEACAS" + app, "fortran")
                    )

            if "+legacy" in spec:
                # Legacy applications -- all are fortran-based except Nemesis
                options.append(define(project_name_base + "_ENABLE_SEACASNemesis", True))

                for app in (
                    "Algebra",
                    "Blot",
                    "Ex1ex2v2",
                    "Ex2ex1v2",
                    "Exomatlab",
                    "Exotec2",
                    "Exotxt",
                    "Fastq",
                    "Gen3D",
                    "Genshell",
                    "Gjoin",
                    "Mapvar",
                    "Mapvar-kd",
                    "Numbers",
                    "Txtexo",
                ):
                    options.append(
                        from_variant(project_name_base + "_ENABLE_SEACAS" + app, "fortran")
                    )

        # ##################### Dependencies ##########################
        # Always need NetCDF-C
        options.extend(
            [define("TPL_ENABLE_Netcdf", True), define("NetCDF_ROOT", spec["netcdf-c"].prefix)]
        )

        if "+parmetis" in spec:
            options.extend(
                [
                    define("TPL_ENABLE_METIS", True),
                    define("METIS_LIBRARY_DIRS", spec["metis"].prefix.lib),
                    define("METIS_LIBRARY_NAMES", "metis"),
                    define("TPL_METIS_INCLUDE_DIRS", spec["metis"].prefix.include),
                    define("TPL_ENABLE_ParMETIS", True),
                    define(
                        "ParMETIS_LIBRARY_DIRS",
                        [spec["parmetis"].prefix.lib, spec["metis"].prefix.lib],
                    ),
                    define("ParMETIS_LIBRARY_NAMES", ["parmetis", "metis"]),
                    define(
                        "TPL_ParMETIS_INCLUDE_DIRS",
                        [spec["parmetis"].prefix.include, spec["metis"].prefix.include],
                    ),
                ]
            )
        elif "+metis" in spec:
            options.extend(
                [
                    define("TPL_ENABLE_METIS", True),
                    define("METIS_LIBRARY_DIRS", spec["metis"].prefix.lib),
                    define("METIS_LIBRARY_NAMES", "metis"),
                    define("TPL_METIS_INCLUDE_DIRS", spec["metis"].prefix.include),
                    define("TPL_ENABLE_ParMETIS", False),
                ]
            )
        else:
            options.extend(
                [define("TPL_ENABLE_METIS", False), define("TPL_ENABLE_ParMETIS", False)]
            )

        options.append(from_variant("TPL_ENABLE_Matio", "matio"))
        if "+matio" in spec:
            options.append(define("Matio_ROOT", spec["matio"].prefix))

        options.append(from_variant("TPL_ENABLE_CGNS", "cgns"))
        if "+cgns" in spec:
            options.append(define("CGNS_ROOT", spec["cgns"].prefix))

        options.append(from_variant("TPL_ENABLE_Faodel", "faodel"))
        for pkg in ("Faodel", "BOOST"):
            if pkg.lower() in spec:
                options.append(define(pkg + "_ROOT", spec[pkg.lower()].prefix))

        options.append(from_variant("TPL_ENABLE_ADIOS2", "adios2"))
        if "+adios2" in spec:
            options.append(define("ADIOS2_ROOT", spec["adios2"].prefix))

        # ################# RPath Handling ######################
        if sys.platform == "darwin" and macos_version() >= Version("10.12"):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append(define("CMAKE_MACOSX_RPATH", True))
        else:
            options.append(define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib))

        return options
