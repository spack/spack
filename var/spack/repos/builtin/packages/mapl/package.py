# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess

from spack.package import *


class Mapl(CMakePackage):
    """
    MAPL is a foundation layer of the GEOS architecture, whose
    original purpose is to supplement the Earth System Modeling
    Framework (ESMF).  MAPL fills in missing capabilities of ESMF,
    provides higher-level interfaces for common boiler-plate logic,
    and enforces various componentization conventions across ESMF
    gridded components within GEOS.

    """

    homepage = "https://github.com/GEOS-ESM/MAPL"
    url = "https://github.com/GEOS-ESM/MAPL/archive/refs/tags/v2.33.0.tar.gz"
    list_url = "https://github.com/GEOS-ESM/MAPL/tags"
    git = "https://github.com/GEOS-ESM/MAPL.git"

    maintainers(
        "mathomp4",
        "tclune",
        "climbfuji",
        "edwardhartnett",
        "Hang-Lei-NOAA",
        "AlexanderRichert-NOAA",
    )

    version("develop", branch="develop")
    version("main", branch="main")

    version("2.42.0", sha256="9b6c3434919c14ef79004db5f76cb3dd8ef375584227101c230a372bb0470fdd")
    version("2.41.2", sha256="73e1f0961f1b70e8159c0a2ce3499eb5158f3ca6d081f4c7826af7854ebfb44d")
    version("2.41.1", sha256="2b384bd4fbaac1bff4ef009922c436c4ab54832172a5cd4d312ea44e32c1ae7c")
    version("2.41.0", sha256="1142f9395e161174e3ec1654fba8bda1d0bd93edc7438b1927d8f5d7b42a0a86")
    version("2.40.4", sha256="fb843b118d6e56cd4fc4b114c4d6f91956d5c8b3d9389ada56da1dfdbc58904f")
    version("2.40.3", sha256="4b82a314c88a035fc2b91395750aa7950d6bee838786178ed16a3f39a1e45519")
    version("2.40.2", sha256="7327f6f5bce6e09e7f7b930013fba86ee7cbfe8ed4c7c087fc9ab5acbf6640fd")
    version("2.40.1", sha256="6f40f946fabea6ba73b0764092e495505d220455b191b4e454736a0a25ee058c")
    version("2.40.0", sha256="406bc63407ced3cd0cb147f203994fd4d14149fa3b909280ee1e0b2b549e732e")
    version("2.39.7", sha256="f0b02bf3dc1c77dba636f95020e4b858da03214711d3a50bc233df277698755a")
    version("2.39.6", sha256="3c1a838b445c5ae5c80d6912033495a9e696257c6113aead4a13755b6a242883")
    version("2.39.5", sha256="42afac883793cb0f2f40ed2c51bfc9f116803299168cbf055a83b33934d3f6c2")
    version("2.39.4", sha256="681842fda70f21e2b2743b3bf861ea2674862c322b885e69c6c2c926e0f5d09e")
    version("2.39.3", sha256="693310aea86bc3e00aaf3d7230eddee2ab0a994e6a55f857f780230e6b47c7d4")
    version("2.39.2", sha256="7a73a73b51852c988e89950a629201221261466d0b810c686423b7ced6ae491e")
    version("2.39.1", sha256="eef783622c8d69bcdcede427760d994906343c5b15a9f020ed45231e9a312192")
    version("2.39.0", sha256="c6ae4558597fe31c1efe18d9a8fc862a89656c88c02098a01fb40d38782e6fa3")
    version("2.38.1", sha256="4bff1077a12da2c63d7ee7b4dc829984dfbd4e84d357595933100a9fd8dd4028")
    version("2.38.0", sha256="bdfd46a348e776356c2cd0e776861dfa7a484a0075a7ee4066364452e4947e8b")
    version("2.37.3", sha256="48f8972605d7a6f4c75b4fe2b0d597c2269210ee6ca65513629891bea5f8e9a4")
    version("2.37.2", sha256="c156383a75b3b8cb57309e03683ae5ad8da7cd2701ee2a1d63226903d75b81bb")
    version("2.37.1", sha256="d68374d1cb8a8a0cc9c1fb018e8d1d81c9efa29c6ccaccc438023ec3461f83f2")
    version("2.37.0", sha256="ae53d58436d74fa40e3a5a743af9bcd6588a4590c0ef0a57c8317f4c7366b62b")
    version("2.36.0", sha256="0dc6c0e4240ae0db31cc0d58ed0f08f568b073710e5722b292bbe0e8ce9b6786")
    version("2.35.3", sha256="079b97a58f3728e5c9fa2a5dffb872496551a79c1cc544f215f2b0a63c708606")
    version("2.35.2", sha256="12d2c3fa264b702253e4792d858f67002fa04ce1c60db341803bc000abb3b7a2")
    version("2.34.3", sha256="8b750754cf5823771f2149d50f9aef585bcf194ca4635e1807c302d4020077e9")
    version("2.34.2", sha256="e46a763084027fe0f326d515e0648b814a82720948062405e03046531f7bb948")
    version("2.34.1", sha256="d2a504f08a4b416c3993d59630f226925bdaeb71488a1706decc49893dc8bcd0")
    version("2.34.0", sha256="4188df84654beed5c7fc3a96a3fb19289ebfc4020c4e14d52088d2ead2745f73")
    version("2.33.0", sha256="a36680d3186cd0399240e9739f5497310bac3f9563f55f77775acf53fa5491bb")
    version("2.32.0", sha256="f0eaec4b6d2514516a77cf426b656655d66f2e0801e639175dddfbd0648997f3")
    version("2.31.0", sha256="dcee4f0d02cc56c29437ab0dfc2f1ae78acce3af84630a55136f8e3626ce36c9")
    version("2.30.3", sha256="52bf65fcd5530079dab32ad1127fbaed940e218a99a89ac5bc8f8330b2094962")
    version("2.30.2", sha256="508b6d0e42593dbedbbb2524bafe7340be7306f80479fde2e4d55868a29753e7")
    version("2.30.1", sha256="df691ac12422184f05f37cb926541d18577ce129e0d6f10e91c90c3922bff572")
    version("2.30.0", sha256="71c469d4618ae97813f784208a102a38c4a30d5ff6301c08cb4fdbd1b1931202")
    version("2.29.0", sha256="aeca5258bc88526895715e3fd3604d43916b5143e948866fea4c1a608120598d")
    version("2.28.0", sha256="3a1f0c9b8b5a1932b2f036deb5463ddbef58a472ee4759c6cc3a4a871b8fe613")
    version("2.27.1", sha256="1aeca20b49729d0212bca764510cb069839d1f2b702c46c8b29a6b2535b2052c")
    version("2.27.0", sha256="a322257522f7fb2768668c02272ae8246ba4be81aa41d8015ce947ba871ce3fb")
    version("2.26.0", sha256="4ef9a1eeffc0521bd6fb4ea5ab261e07d3b5a46f0a6c43673ee169bf0d624bb8")
    version("2.25.0", sha256="f3ce71004f4274cedee28852cc105e0bf51a86cafc4d5f5af9de6492c4be9402")
    version("2.24.0", sha256="cd15ffd6897c18e64267e5fa86523402eb48cbf638ad5f3b4b5b0ff8939d1936")
    version("2.23.1", sha256="563f3e9f33adae298835e7de7a4a29452a2a584d191248c59494c49d3ee80d24")
    version("2.23.0", sha256="ae25ec63d0f288599c668f35fdbccc76abadbfc6d48f95b6eb4e7a2c0c69f241")
    version("2.22.0", sha256="3356b8d29813431d272c5464e265f3fe3ce1ac7f49ae6d41da34fe4b82aa691a")
    version(
        "2.12.3",
        sha256="e849eff291939509e74830f393cb2670c2cc96f6160d8060dbeb1742639c7d41",
        deprecated=True,
    )
    version(
        "2.11.0",
        sha256="76351e026c17e2044b89085db639e05ba0e7439a174d14181e01874f0f93db44",
        deprecated=True,
    )
    version(
        "2.8.1",
        sha256="a7657d4c52a66c3a6663e436d2c2dd4dbb81addd747e1ace68f59843665eb739",
        deprecated=True,
    )
    version(
        "2.8.0",
        sha256="6da60a21ab77ecebc80575f25b756c398ef48f635ab0b9c96932a1d4ebd8b4a0",
        deprecated=True,
    )
    version(
        "2.7.3",
        sha256="e8cdc0816471bb4c42673c2fa66d9d749f5a18944cd31580a2d6fd6d961ba163",
        deprecated=True,
    )
    version(
        "2.7.2",
        sha256="8f123352c665c434a18ff87304a71a61fb3342919adcccfea2a40729992d9f93",
        deprecated=True,
    )
    version(
        "2.7.1",
        sha256="8239fdbebd2caa47a232c24927f7a91196704e35c8b7909e1bbbefccf0647ea6",
        deprecated=True,
    )

    # Versions later than 3.14 remove FindESMF.cmake
    # from ESMA_CMake.
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.36.0",
        when="@2.42.0:",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.31.0",
        when="@2.40.0:",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.28.0",
        when="@2.36.0:2.39",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.24.0",
        when="@2.34.0:2.35",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.21.0",
        when="@2.22.0:2.33",
    )
    # NOTE: Remove this resource(), the patch() commands below
    # and the actual patches when MAPL 2.12 and older are deleted
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.13.0",
        when="@:2.12.3",
    )

    # Patch to configure Apple M1 chip in x86_64 Rosetta 2 emulator mode
    # Needed for versions earlier than 3.14 of ESMA_cmake only.
    patch("esma_cmake_apple_m1_rosetta.patch", when="@:2.12.3")

    # Patch to add missing NetCDF C target in various CMakeLists.txt
    patch("mapl-2.12.3-netcdf-c.patch", when="@:2.12.3")

    # Patch to add missing MPI Fortran target to top-level CMakeLists.txt
    patch("mapl-2.12.3-mpi-fortran.patch", when="@:2.12.3")

    # MAPL only compiles with MPICH from version 2.42.0 and higher so we conflict
    # with older versions. Also, it's only been tested with MPICH 4, so we don't
    # allow older MPICH
    conflicts("mpich@:3")
    conflicts("mpich@4", when="@:2.41")

    variant("flap", default=False, description="Build with FLAP support", when="@:2.39")
    variant("pflogger", default=True, description="Build with pFlogger support")
    variant("fargparse", default=True, description="Build with fArgParse support")
    variant("shared", default=True, description="Build as shared library")
    variant("debug", default=False, description="Make a debuggable version of the library")
    variant("extdata2g", default=True, description="Use ExtData2G")
    variant("pfunit", default=False, description="Build with pFUnit support")
    variant("f2py", default=False, description="Build with f2py support")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "Aggressive"),
    )

    depends_on("cmake@3.17:", type="build")
    depends_on("mpi")
    depends_on("hdf5")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("esmf@8.5:", when="@2.40:")
    depends_on("esmf@8.4", when="@2.34:2.39")
    depends_on("esmf@8.3", when="@2.22:2.33")
    depends_on("esmf", when="@:2.12.99")
    depends_on("esmf~debug", when="~debug")
    depends_on("esmf+debug", when="+debug")

    depends_on("gftl@1.10.0:", when="@2.40:")
    depends_on("gftl@1.5.5:1.9", when="@:2.39")

    # There was an interface change in gftl-shared, so we need to control versions
    # MAPL 2.39 and older can use up to 1.6.0 but MAPL 2.40+ needs 1.6.1 or higher
    depends_on("gftl-shared@1.6.1:", when="@2.40:")
    depends_on("gftl-shared@1.3.1:1.6.0", when="@:2.39")

    # There was an interface change in yaFyaml, so we need to control versions
    # MAPL 2.22 and older uses older version, MAPL 2.23+ and higher uses newer
    # Note that MAPL 2.40+ no longer require yafyaml as we get yaml support
    # via esmf 8.5.0
    depends_on("yafyaml@1.0-beta5", when="@:2.22+extdata2g")
    depends_on("yafyaml@1.0.4:", when="@2.23:2.39+extdata2g")

    # pFlogger depends on yaFyaml in the same way. MAPL 2.22 and below uses old
    # yaFyaml so we need to use old pFlogger, but MAPL 2.23+ uses new yaFyaml
    depends_on("pflogger@:1.6 +mpi", when="@:2.22+pflogger")
    depends_on("pflogger@1.9.1: +mpi", when="@2.23:2.39+pflogger")
    depends_on("pflogger@1.9.5: +mpi", when="@2.40:+pflogger")

    # fArgParse v1.4.1 is the first usable version with MAPL
    # we now require 1.5.0 with MAPL 2.40+
    depends_on("fargparse@1.5.0:", when="@2.40:+fargparse")
    depends_on("fargparse@1.4.1:1.4", when="@:2.39+fargparse")

    depends_on("pfunit@4.2: +mpi +fhamcrest", when="+pfunit")
    depends_on("flap", when="+flap")

    depends_on("ecbuild", type="build")

    depends_on("python@3:")
    depends_on("py-numpy", when="+f2py")
    depends_on("perl")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_WITH_FLAP", "flap"),
            self.define_from_variant("BUILD_WITH_PFLOGGER", "pflogger"),
            self.define_from_variant("BUILD_WITH_FARGPARSE", "fargparse"),
            self.define_from_variant("BUILD_SHARED_MAPL", "shared"),
            self.define_from_variant("USE_EXTDATA2G", "extdata2g"),
            self.define_from_variant("USE_F2PY", "f2py"),
            "-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc,
        ]

        if self.spec.satisfies("@2.22.0:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["esmf"].prefix.cmake))

        # Compatibility flags for gfortran
        fflags = []
        if self.compiler.name in ["gcc", "clang", "apple-clang"]:
            fflags.append("-ffree-line-length-none")
            gfortran_major_ver = int(
                spack.compiler.get_compiler_version_output(self.compiler.fc, "-dumpversion").split(
                    "."
                )[0]
            )
            if gfortran_major_ver >= 10:
                fflags.append("-fallow-invalid-boz")
                fflags.append("-fallow-argument-mismatch")
        if fflags:
            args.append(self.define("CMAKE_Fortran_FLAGS", " ".join(fflags)))

        return args

    def patch(self):
        if "~shared" in self.spec["netcdf-c"]:
            nc_pc_cmd = ["nc-config", "--static", "--libs"]
            nc_flags = subprocess.check_output(nc_pc_cmd, encoding="utf8").strip()
            filter_file(
                "(target_link_libraries[^)]+PUBLIC )", r"\1 %s " % nc_flags, "pfio/CMakeLists.txt"
            )

    def setup_build_environment(self, env):
        # esma_cmake, an internal dependency of mapl, is
        # looking for the cmake argument -DBASEDIR, and
        # if it doesn't find it, it's looking for an
        # environment variable with the same name. This
        # name is common and used all over the place,
        # and if it is set it breaks the mapl build.
        env.unset("BASEDIR")
