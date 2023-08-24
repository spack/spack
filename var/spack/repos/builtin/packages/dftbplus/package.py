# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dftbplus(MakefilePackage, CMakePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    # url = "https://github.com/dftbplus/dftbplus/archive/19.1.tar.gz"
    git = "https://github.com/dftbplus/dftbplus.git"
    version("23.1", tag="23.1", submodules=True)
    version("22.2", tag="22.2", submodules=True)
    version("22.1", tag="22.1", submodules=True)
    version("21.2", tag="21.2", submodules=True)
    version("21.1", tag="21.1", submodules=True)
    version("20.2", tag="20.2", submodules=True)
    version("20.1", tag="20.1", submodules=True)  # This and higher version uses Cmake
    version('19.1', tag='19.1', submodules=True)
    # version("19.1", sha256="4d07f5c6102f06999d8cfdb1d17f5b59f9f2b804697f14b3bc562e3ea094b8a8")

    build_system(
        conditional("cmake", when="@20.1:"),
        conditional("makefile", when="@:19.1"),
        default="cmake",
    )

    resource(
        name="slakos",
        url="https://github.com/dftbplus/testparams/archive/dftbplus-18.2.tar.gz",
        sha256="bd191b3d240c1a81a8754a365e53a78b581fc92eb074dd5beb8b56a669a8d3d1",
        destination="external/slakos",
        when="@18.2:",
    )

    variant("mpi", default=True, description="Build an MPI-paralelised version of the code.")

    variant(
        "gpu",
        default=False,
        description="Use the MAGMA library " "for GPU accelerated computation",
    )

    variant(
        "elsi",
        default=False,
        description="Use the ELSI library for large scale systems. "
        "Only has any effect if you build with '+mpi'",
    )

    variant(
        "sockets",
        default=False,
        description="Whether the socket library " "(external control) should be linked",
    )

    variant("arpack", default=False, description="Use ARPACK for excited state DFTB functionality")

    variant(
        "transport",
        default=False,
        description="Whether transport via libNEGF should be included. "
        "Only affects parallel build. "
        "(serial version is built without libNEGF/transport)",
    )

    variant(
        "dftd3",
        default=False,
        description="Use DftD3 dispersion library " "(if you need this dispersion model)",
    )
    variant(
        "api",
        default=True,
        description="Build the API library " "(if you need to link to DFTB+ from other codes)",
        when="build_system=cmake",
    )
    variant(
        "openmp",
        default=True,
        description="Build with OpenMP support " "(if you need to use OpenMP parallelization)",
    )
    variant(
        "sharedlibs",
        default=False,
        description="Build as shared library",
    )

    depends_on("lapack")
    depends_on("blas")
    depends_on("scalapack", when="+mpi")
    depends_on("mpi", when="+mpi")
    depends_on("elsi", when="+elsi")
    depends_on("magma", when="+gpu")
    depends_on("arpack-ng", when="+arpack~mpi")
    depends_on("dftd3-lib@0.9.2", when="+dftd3")
    depends_on("m4", type="build", when="@:19.1")
    depends_on("python@3.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))  # for tests
    depends_on("cmake", type="build", when="@20.1:")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
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

class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        # Note: dftbplus@20.1 uses plural form of the option names
        #       (e.g. -DSCALAPACK_LIBRARIES)
        # but dftbplus@20.2 onwards uses singular
        #       (e.g. -DSCALAPACK_LIBRARY)
        # and plural form is ignored.
        # We set both inorder to be compatible with all versions.

        spec = self.spec
        lapack_libs = spec["lapack"].libs.joined(";")
        blas_libs = spec["blas"].libs.joined(";")
        args = [
            self.define_from_variant("WITH_OPENMP", "openmp"),
            self.define_from_variant("WITH_MPI", "mpi"),
            self.define("LAPACK_FOUND", True),
            self.define("LAPACK_INCLUDE_DIRS", spec["lapack"].prefix.include),
            self.define("LAPACK_LIBRARIES", lapack_libs),
            self.define("BLAS_FOUND", True),
            self.define("BLAS_INCLUDE_DIRS", spec["blas"].prefix.include),
            self.define("BLAS_LIBRARIES", blas_libs),
            self.define("BLAS_LIBRARY", blas_libs),
            self.define_from_variant("WITH_ELSI", "elsi"),
            self.define_from_variant("WITH_GPU", "gpu"),
            self.define_from_variant("WITH_TRANSPORT", "transport"),
            self.define_from_variant("WITH_SOCKETS", "sockets"),
            self.define_from_variant("WITH_ARPACK", "arpack"),
            self.define_from_variant("WITH_DFTD3", "dftd3"),
            self.define_from_variant("WITH_API", "api"),
            self.define_from_variant("BUILD_SHARED_LIBS", "sharedlibs"),
        ]
        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_Fortran_COMPILER", spec["mpi"].mpifc))
            args.append(self.define("SCALAPACK_LIBRARY",  spec["scalapack"].libs.joined(";")))
            args.append(self.define("SCALAPACK_LIBRARIES", spec["scalapack"].libs.joined(";")))
            args.append(self.define("SCALAPACK_INCLUDE_DIR", spec["scalapack"].prefix.include))
        return args