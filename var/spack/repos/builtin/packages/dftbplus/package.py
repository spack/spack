# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dftbplus(CMakePackage, MakefilePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    url = "https://github.com/dftbplus/dftbplus/releases/download/22.1/dftbplus-22.1.tar.xz"
    git = "https://github.com/dftbplus/dftbplus.git"

    maintainers = ["HaoZeke", "aradi", "iamashwin99"]
    generator = "Ninja"

    build_system(
        conditional("cmake", when="@20.1:"),
        conditional("makefile", when="@:19.1"),
        default="cmake",
    )

    version("main", branch="main")
    version("22.1", sha256="f0fc9a076aa2d7be03c31a3a845d8151fc0cc0b1d421e11c37044f78a42abb33")
    version("21.2", sha256="e73aa698ff951b59f7fe2ea027b292bae16abf545c9fdbb11b5b5127f04a3c10")
    version("21.1", sha256="31d5a488843a05d8589a375307a2832c1fc938f9f7d830c45a062726659e7b0a")
    version("20.2.1", sha256="6b1827a45b20d1757119a75abcb851cd4362e7abc58601094d029ed5922d6da7")
    version("20.2", sha256="6b1f10c7efbdaf59acf64d8fb8afc80460c0fbc6c4dbe256b760223cbd28ed2c")
    version("20.1", sha256="a155ca927c804234587c61c4938d154f31578c816b0ce20eaee3b5d7e39d91dc")
    version(
        "19.1",
        sha256="4d07f5c6102f06999d8cfdb1d17f5b59f9f2b804697f14b3bc562e3ea094b8a8",
        deprecated=True,
    )

    variant(
        "api",
        default=True,
        description="Whether public API should be included and the DFTB+ library installed.",
    )
    variant(
        "arpack",
        default=False,
        description="Whether the ARPACK library should be included (needed for TD-DFTB).",
    )
    variant(
        "chimes",
        default=False,
        when="@21.2:",
        description="Whether repulsive corrections" "via the ChIMES library should be enabled.",
    )
    variant(
        "elsi",
        default=False,
        description="Use the ELSI library for large scale systems. "
        "Only has any effect if you build with '+mpi'",
    )
    variant(
        "gpu",
        default=False,
        description="Use the MAGMA library " "for GPU accelerated computation",
    )
    variant(
        "mbd",
        default=False,
        when="21.1:",
        description="Whether DFTB+ should be built with many-body-dispersion support.",
    )
    variant("mpi", default=False, description="Whether DFTB+ should support MPI-parallelism.")
    variant(
        "openmp",
        default=True,
        description="Whether OpenMP thread parallisation should be enabled.",
    )
    variant(
        "plumed",
        default=False,
        when="@20.1:",
        description="Whether metadynamics via the PLUMED2 library should be allowed.",
    )
    variant("poisson", default=False, description="Whether the Poisson-solver should be included.")
    variant(
        "python",
        default=False,
        description="Whether the Python components of DFTB+ should be tested and installed.",
    )
    variant(
        "sdftd3",
        default=False,
        when="@21.2:",
        description="Whether the s-dftd3 library should be included",
    )
    variant(
        "sockets",
        default=False,
        description="Whether the socket library " "(external control) should be linked",
    )
    variant(
        "transport",
        default=False,
        description="Whether transport via libNEGF should be included. "
        "Only affects parallel build. "
        "(serial version is built without libNEGF/transport)",
    )
    variant(
        "tblite",
        default=False,
        when="@21.2:",
        description="Whether xTB support should be included via tblite.",
    )

    variant("shared", default=False, description="Most often for the Python wrappers.")

    # ONLY for version 19.1
    variant(
        "dftd3",
        default=False,
        when="@:21.1",
        description="Use DftD3 dispersion library " "(if you need this dispersion model)",
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja@1.10", type="build")

    depends_on("blas", when="-mpi")
    depends_on("lapack", when="-mpi")

    depends_on("arpack-ng", when="+arpack~mpi")
    depends_on("simple-dftd3", when="+sdftd3")
    depends_on("elsi", when="+elsi")
    depends_on("magma", when="+gpu")
    depends_on("mpi", when="+mpi")
    depends_on("plumed", when="+plumed")
    depends_on("scalapack", when="+mpi")
    depends_on("python", when="+python")
    # Only for 19.1
    depends_on("dftd3-lib@0.9.2", when="+dftd3")

    # Conflicts
    conflicts("+python", when="~shared")
    conflicts("-poisson", when="+transport")

    # Extensions
    extends("python", when="+python")

    @when("@19.1")  # Only version without CMake
    def edit(self, spec, prefix):
        """
        First, change the ROOT variable, because, for some reason,
        the Makefile and the spack install script run in different directories
        Then, if using GCC, rename the file 'sys/make.x86_64-linux-gnu'
        to make.arch.
        After that, edit the make.arch to point to the dependencies
        And the last thing we do here is to set the installdir
        """
        dircwd = os.getcwd()
        makefile = FileFilter("makefile")
        makefile.filter("ROOT := .*", "ROOT := {0}".format(dircwd))

        archmake = join_path(".", "sys", "make.x86_64-linux-gnu")
        copy(archmake, join_path(dircwd, "make.arch"))

        march = FileFilter(join_path(dircwd, "make.arch"))

        mconfig = FileFilter(join_path(dircwd, "make.config"))

        mconfig.filter("INSTALLDIR := .*", "INSTALLDIR := {0}".format(prefix))

        if "+gpu" in self.spec:
            march.filter("MAGMADIR = .*", "MAGMADIR = {0}".format(spec["magma"].prefix))

            mconfig.filter("WITH_GPU := .*", "WITH_GPU := 1")

        if "+mpi" in self.spec:
            march.filter(
                "SCALAPACKDIR = .*", "SCALAPACKDIR = {0}".format(spec["scalapack"].prefix)
            )

            march.filter(
                "LIB_LAPACK = -l.*", "LIB_LAPACK = {0}".format(spec["blas"].libs.ld_flags)
            )

            march.filter("mpifort", "{0}".format(spec["mpi"].mpifc))

            mconfig.filter("WITH_MPI := .*", "WITH_MPI := 1")

            if "+elsi" in self.spec:
                mconfig.filter("WITH_ELSI := .*", "WITH_ELSI := 1")

                has_pexsi = "+enable_pexsi" in spec["elsi"]

                mconfig.filter(
                    "WITH_PEXSI := .*",
                    "WITH_PEXSI := {0}".format("1" if has_pexsi is True else "0"),
                )

                march.filter(
                    "ELSIINCDIR .*", "ELSIINCDIR = {0}".format(spec["elsi"].prefix.include)
                )

                march.filter("ELSIDIR .*", "ELSIDIR = {0}".format(spec["elsi"].prefix))

        else:
            march.filter(
                "LIB_LAPACK += -l.*", "LIB_LAPACK += {0}".format(spec["blas"].libs.ld_flags)
            )

        if "+sockets" in self.spec:
            mconfig.filter("WITH_SOCKETS := .*", "WITH_SOCKETS := 1")

        if "+transport" in self.spec:
            mconfig.filter("WITH_TRANSPORT := .*", "WITH_TRANSPORT := 1")

        if "+arpack" in self.spec:
            march.filter(
                "ARPACK_LIBS = .*", "ARPACK_LIBS = {0}".format(spec["arpack-ng"].libs.ld_flags)
            )

            mconfig.filter("WITH_ARPACK := .*", "WITH_ARPACK := 1")

        if "+dftd3" in self.spec:
            march.filter("COMPILE_DFTD3 = .*", "COMPILE_DFTD3 = 0")
            march.filter(
                "DFTD3_INCS = .*", "DFTD3_INCS = -I{0}".format(spec["dftd3-lib"].prefix.include)
            )

            march.filter(
                "DFTD3_LIBS = .*", "DFTD3_LIBS = -L{0} -ldftd3".format(spec["dftd3-lib"].prefix)
            )

            mconfig.filter("WITH_DFTD3 := .*", "WITH_DFTD3 := 1")

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_OPENMP", "openmp"),
            self.define_from_variant("WITH_API", "api"),
            self.define_from_variant("WITH_ARPACK", "arpack"),
            self.define_from_variant("WITH_CHIMES", "chimes"),
            self.define_from_variant("WITH_ELSI", "elsi"),
            self.define_from_variant("WITH_GPU", "gpu"),
            self.define_from_variant("WITH_MBD", "mbd"),
            self.define_from_variant("WITH_MPI", "mpi"),
            self.define_from_variant("WITH_PLUMED", "plumed"),
            self.define_from_variant("WITH_POISSON", "poisson"),
            self.define_from_variant("WITH_PYTHON", "python"),
            self.define_from_variant("WITH_SDFTD3", "sdftd3"),
            self.define_from_variant("WITH_SOCKETS", "sockets"),
            self.define_from_variant("WITH_TBLITE", "tblite"),
            self.define_from_variant("WITH_TRANSPORT", "transport"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        # SCALAPACK
        if "+mpi" in self.spec:
            args.extend(
                [
                    self.define("SCALAPACK_FOUND", "true"),
                    self.define("SCALAPACK_INCLUDE_DIRS", self.spec["scalapack"].prefix.include),
                    self.define("SCALAPACK_LIBRARIES", self.spec["scalapack"].libs.joined(";")),
                    self.define("SCALAPACK_LIBRARY", self.spec["scalapack"].libs.joined(";")),
                ]
            )
        if "+python" in self.spec:
            args.append(self.define("BUILD_SHARED_LIBS", True))
        if self.run_tests:
            args.append("-DWITH_UNIT_TESTS=ON")
        else:
            args.append("-DWITH_UNIT_TESTS=OFF")
        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Run ctest after building binary.
        only run the unit tests. If the unit tests fail, the installation throws
        a warning."""

        with working_dir(self.build_directory):
            try:
                ctest("")
            except ProcessError:
                warn = "Unit tests failed.\n"
                warn += "Please report this failure to:\n"
                warn += "https://github.com/dftbplus/dftbplus/issues"
                tty.msg(warn)
