# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.build_environment import dso_suffix, stat_suffix
from spack.package import *


class Esmf(MakefilePackage):
    """The Earth System Modeling Framework (ESMF) is high-performance, flexible
    software infrastructure for building and coupling weather, climate, and
    related Earth science applications. The ESMF defines an architecture for
    composing complex, coupled modeling systems and includes data structures
    and utilities for developing individual models."""

    homepage = "https://www.earthsystemcog.org/projects/esmf/"
    url = "https://github.com/esmf-org/esmf/archive/ESMF_8_0_1.tar.gz"
    git = "https://github.com/esmf-org/esmf.git"

    maintainers("climbfuji", "jedwards4b", "AlexanderRichert-NOAA")

    # Develop is a special name for spack and is always considered the newest version
    version("develop", branch="develop")
    # generate chksum with spack checksum esmf@x.y.z
    version("8.4.0", sha256="28531810bf1ae78646cda6494a53d455d194400f19dccd13d6361871de42ed0f")
    version("8.3.1", sha256="6c39261e55dcdf9781cdfa344417b9606f7f961889d5ec626150f992f04f146d")
    version("8.3.0", sha256="0ff43ede83d1ac6beabd3d5e2a646f7574174b28a48d1b9f2c318a054ba268fd")
    version("8.3.0b09", commit="5b7e546c4b")
    version("8.2.0", sha256="3693987aba2c8ae8af67a0e222bea4099a48afe09b8d3d334106f9d7fc311485")
    version("8.1.1", sha256="58c2e739356f21a1b32673aa17a713d3c4af9d45d572f4ba9168c357d586dc75")
    version("8.0.1", sha256="9172fb73f3fe95c8188d889ee72fdadb4f978b1d969e1d8e401e8d106def1d84")
    version("8.0.0", sha256="051dca45f9803d7e415c0ea146df15ce487fb55f0fce18ca61d96d4dba0c8774")
    version("7.1.0r", sha256="ae9a5edb8d40ae97a35cbd4bd00b77061f995c77c43d36334dbb95c18b00a889")

    variant("mpi", default=True, description="Build with MPI support")
    variant("external-lapack", default=False, description="Build with external LAPACK support")
    variant("netcdf", default=True, description="Build with NetCDF support")
    variant("pnetcdf", default=True, description="Build with pNetCDF support", when="+mpi")
    variant("xerces", default=True, description="Build with Xerces support")
    variant(
        "parallelio",
        default=True,
        description="Build with external parallelio library",
        when="@8.3:",
    )
    variant(
        "parallelio",
        default=False,
        description="Build with external parallelio library",
        when="@8.3.b09",
    )
    variant("pio", default=True, description="Enable Internal ParallelIO support", when="@:8.2.99")
    variant(
        "pio", default=True, description="Enable Internal ParallelIO support", when="@8.3.0b09"
    )
    variant("debug", default=False, description="Make a debuggable version of the library")
    variant("shared", default=True, description="Build shared library")
    # 'esmf_comm' and 'esmf_os' variants allow override values for their corresponding
    # build environment variables. Documentation, including valid values, can be found at
    # https://earthsystemmodeling.org/docs/release/latest/ESMF_usrdoc/node10.html#SECTION000105000000000000000
    variant("esmf_comm", default="auto", description="Override for ESMF_COMM variable")
    variant("esmf_os", default="auto", description="Override for ESMF_OS variable")

    # Required dependencies
    depends_on("zlib")
    depends_on("libxml2")

    # Optional dependencies
    depends_on("mpi", when="+mpi")
    depends_on("lapack@3:", when="+external-lapack")
    depends_on("netcdf-c@3.6:", when="+netcdf")
    depends_on("netcdf-fortran@3.6:", when="+netcdf")
    depends_on("parallel-netcdf@1.2.0:", when="+pnetcdf")
    depends_on("xerces-c@3.1.0:", when="+xerces")
    depends_on("parallelio@2.5.8:", when="+parallelio")

    # Testing dependencies
    depends_on("perl", type="test")

    # Make esmf build with newer intel versions
    patch("intel.patch", when="@:7.0 %intel@17:")
    # Make esmf build with newer gcc versions
    # https://sourceforge.net/p/esmf/esmf/ci/3706bf758012daebadef83d6575c477aeff9c89b/
    patch("gcc.patch", when="@:7.0 %gcc@6:")

    # Fix undefined reference errors with mvapich2
    # https://sourceforge.net/p/esmf/esmf/ci/34de0ccf556ba75d35c9687dae5d9f666a1b2a18/
    patch("mvapich2.patch", when="@:7.0")

    # explicit type cast of variables from long to int
    patch("longtoint.patch", when="@:8.3.2 %cce@14:")
    patch("longtoint.patch", when="@:8.3.2 %oneapi@2022:")

    # Allow different directories for creation and
    # installation of dynamic libraries on OSX:
    patch("darwin_dylib_install_name.patch", when="platform=darwin @:7.0")

    # Missing include file for newer gcc compilers
    # https://trac.macports.org/ticket/57493
    patch("cstddef.patch", when="@7.1.0r %gcc@8:")

    # Make script from mvapich2.patch executable
    @when("@:7.0")
    @run_before("build")
    def chmod_scripts(self):
        chmod = which("chmod")
        chmod("+x", "scripts/libs.mvapich2f90")

    def url_for_version(self, version):
        if version < Version("8.0.0"):
            return "http://www.earthsystemmodeling.org/esmf_releases/public/ESMF_{0}/esmf_{0}_src.tar.gz".format(
                version.underscored
            )
        elif version < Version("8.2.1"):
            return "https://github.com/esmf-org/esmf/archive/ESMF_{0}.tar.gz".format(
                version.underscored
            )
        else:
            # Starting with ESMF 8.2.1 releases are now in the form vx.y.z
            return "https://github.com/esmf-org/esmf/archive/refs/tags/v{0}.tar.gz".format(
                version.dotted
            )

    def setup_build_environment(self, env):
        spec = self.spec
        # Installation instructions can be found at:
        # http://www.earthsystemmodeling.org/esmf_releases/last_built/ESMF_usrdoc/node9.html

        # Unset any environment variables that may influence the installation.
        for var in os.environ:
            if var.startswith("ESMF_"):
                env.unset(var)

        ######################################
        # Build and Installation Directories #
        ######################################

        # The environment variable ESMF_DIR must be set to the full pathname
        # of the top level ESMF directory before building the framework.
        env.set("ESMF_DIR", self.stage.source_path)

        # This variable specifies the prefix of the installation path used
        # with the install target.
        env.set("ESMF_INSTALL_PREFIX", prefix)

        # Installation subdirectories default to:
        # bin/binO/Linux.gfortran.64.default.default
        env.set("ESMF_INSTALL_BINDIR", "bin")
        env.set("ESMF_INSTALL_LIBDIR", "lib")
        env.set("ESMF_INSTALL_MODDIR", "include")

        # Allow compiler flags to carry through from compiler spec
        env.set("ESMF_CXXCOMPILEOPTS", " ".join(spec.compiler_flags["cxxflags"]))
        env.set("ESMF_F90COMPILEOPTS", " ".join(spec.compiler_flags["fflags"]))
        # ESMF will simply not build with Intel using backing GCC 8, in that
        # case you need to point to something older, below is commented but is
        # an example
        # env.set("ESMF_CXXCOMPILEOPTS", "-O2 -std=c++11 -gcc-name=/usr/bin/gcc")
        # env.set("ESMF_F90COMPILEOPTS", "-O2 -gcc-name=/usr/bin/gcc")

        ############
        # Compiler #
        ############

        # ESMF_COMPILER must be set to select which Fortran and
        # C++ compilers are being used to build the ESMF library.
        if self.compiler.name == "gcc":
            env.set("ESMF_COMPILER", "gfortran")
            gfortran_major_version = int(
                spack.compiler.get_compiler_version_output(self.compiler.fc, "-dumpversion").split(
                    "."
                )[0]
            )
        elif self.compiler.name == "intel" or self.compiler.name == "oneapi":
            env.set("ESMF_COMPILER", "intel")
        elif self.compiler.name in ["clang", "apple-clang"]:
            env.set("ESMF_COMPILER", "gfortranclang")
            gfortran_major_version = int(
                spack.compiler.get_compiler_version_output(self.compiler.fc, "-dumpversion").split(
                    "."
                )[0]
            )
        elif self.compiler.name == "nag":
            env.set("ESMF_COMPILER", "nag")
        elif self.compiler.name == "pgi":
            env.set("ESMF_COMPILER", "pgi")
        elif self.compiler.name == "nvhpc":
            env.set("ESMF_COMPILER", "nvhpc")
        elif self.compiler.name == "cce":
            env.set("ESMF_COMPILER", "cce")
        else:
            msg = "The compiler you are building with, "
            msg += '"{0}", is not supported by ESMF.'
            raise InstallError(msg.format(self.compiler.name))

        if "+mpi" in spec:
            env.set("ESMF_CXX", spec["mpi"].mpicxx)
            env.set("ESMF_F90", spec["mpi"].mpifc)
        else:
            env.set("ESMF_CXX", spack_cxx)
            env.set("ESMF_F90", spack_fc)

        # This environment variable controls the build option.
        if "+debug" in spec:
            # Build a debuggable version of the library.
            env.set("ESMF_BOPT", "g")
        else:
            # Build an optimized version of the library.
            env.set("ESMF_BOPT", "O")

        if self.compiler.name in ["gcc", "clang", "apple-clang"] and gfortran_major_version >= 10:
            env.set("ESMF_F90COMPILEOPTS", "-fallow-argument-mismatch")

        #######
        # OS  #
        #######

        # ESMF_OS must be set for Cray systems
        # But spack no longer gives arch == cray
        if self.compiler.name == "cce" or "^cray-mpich" in self.spec:
            env.set("ESMF_OS", "Unicos")

        # Allow override of ESMF_OS:
        os_variant = spec.variants["esmf_os"].value
        if os_variant != "auto":
            env.set("ESMF_OS", os_variant)

        #######
        # MPI #
        #######

        # ESMF_COMM must be set to indicate which MPI implementation
        # is used to build the ESMF library.
        if "+mpi" in spec:
            if "^cray-mpich" in self.spec:
                env.set("ESMF_COMM", "mpi")
            elif "^mvapich2" in spec:
                env.set("ESMF_COMM", "mvapich2")
            elif "^mpich" in spec:
                # esmf@7.0.1 does not include configs for mpich3,
                # so we start with the configs for mpich2:
                env.set("ESMF_COMM", "mpich2")
                # The mpich 3 series split apart the Fortran and C bindings,
                # so we link the Fortran libraries when building C programs:
                env.set("ESMF_CXXLINKLIBS", "-lmpifort")
            elif "^openmpi" in spec or "^hpcx-mpi" in spec:
                env.set("ESMF_COMM", "openmpi")
            elif (
                "^intel-parallel-studio+mpi" in spec
                or "^intel-mpi" in spec
                or "^intel-oneapi-mpi" in spec
            ):
                env.set("ESMF_COMM", "intelmpi")
            elif "^mpt" in spec:
                # MPT is the HPE (SGI) variant of mpich
                env.set("ESMF_COMM", "mpt")
        else:
            # Force use of the single-processor MPI-bypass library.
            env.set("ESMF_COMM", "mpiuni")

        # Allow override of ESMF_COMM:
        comm_variant = spec.variants["esmf_comm"].value
        if comm_variant != "auto":
            env.set("ESMF_COMM", comm_variant)

        ##########
        # LAPACK #
        ##########

        if "+external-lapack" in spec:
            # A system-dependent external LAPACK/BLAS installation is used
            # to satisfy the external dependencies of the LAPACK-dependent
            # ESMF code.
            env.set("ESMF_LAPACK", "system")

            # FIXME: determine whether or not we need to set this
            # Specifies the path where the LAPACK library is located.
            # env.set("ESMF_LAPACK_LIBPATH", spec["lapack"].prefix.lib)

            # Specifies the linker directive needed to link the LAPACK library
            # to the application.
            env.set("ESMF_LAPACK_LIBS", spec["lapack"].libs.link_flags)  # noqa
        else:
            env.set("ESMF_LAPACK", "internal")

        ##########
        # NetCDF #
        ##########

        if "+netcdf" in spec:
            # ESMF provides the ability to read Grid and Mesh data in
            # NetCDF format.
            env.set("ESMF_NETCDF", "nc-config")
            env.set("ESMF_NFCONFIG", "nf-config")

        ###################
        # Parallel-NetCDF #
        ###################

        if "+pnetcdf" in spec:
            # ESMF provides the ability to write Mesh weights
            # using Parallel-NetCDF.

            # When defined, enables the use of Parallel-NetCDF.
            # ESMF_PNETCDF_LIBS will be set to "-lpnetcdf".
            env.set("ESMF_PNETCDF", "pnetcdf-config")

        ##############
        # ParallelIO #
        ##############
        if "+parallelio" in spec:
            env.set("ESMF_PIO", "external")
            env.set("ESMF_PIO_LIBPATH", spec["parallelio"].prefix.lib)
            env.set("ESMF_PIO_INCLUDE", spec["parallelio"].prefix.include)
        elif "+pio" in spec and "+mpi" in spec:
            # ESMF provides the ability to read and write data in both binary
            # and NetCDF formats through ParallelIO (PIO), a third-party IO
            # software library that is integrated in the ESMF library.
            # PIO-dependent features will be enabled and will use the
            # PIO library that is included and built with ESMF.
            env.set("ESMF_PIO", "internal")
        else:
            # Disables PIO-dependent code.
            env.set("ESMF_PIO", "OFF")

        ##########
        # XERCES #
        ##########

        if "+xerces" in spec:
            # ESMF provides the ability to read Attribute data in
            # XML file format via the XERCES C++ library.

            # ESMF_XERCES_LIBS will be set to "-lxerces-c".
            env.set("ESMF_XERCES", "standard")

            # FIXME: determine if the following are needed
            # ESMF_XERCES_INCLUDE
            # ESMF_XERCES_LIBPATH

        # Static-only option:
        if "~shared" in spec:
            env.set("ESMF_SHARED_LIB_BUILD", "OFF")

    @run_after("install")
    def post_install(self):
        install_tree("cmake", self.prefix.cmake)
        # Several applications using ESMF are affected by CMake capitalization
        # issue. The following fix allows all apps to use as-is.
        for prefix in [dso_suffix, stat_suffix]:
            library_path = os.path.join(self.prefix.lib, "libesmf.%s" % prefix)
            if os.path.exists(library_path):
                os.symlink(library_path, os.path.join(self.prefix.lib, "libESMF.%s" % prefix))

    def check(self):
        make("check", parallel=False)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("ESMFMKFILE", os.path.join(self.prefix.lib, "esmf.mk"))

    def setup_run_environment(self, env):
        env.set("ESMFMKFILE", os.path.join(self.prefix.lib, "esmf.mk"))
