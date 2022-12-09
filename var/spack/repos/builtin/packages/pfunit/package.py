# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Pfunit(CMakePackage):
    """
    pFUnit is a unit testing framework enabling JUnit-like testing of
    serial and MPI-parallel software written in Fortran.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/pFUnit"
    url = "https://github.com/Goddard-Fortran-Ecosystem/pFUnit/releases/download/v4.6.1/pFUnit-v4.6.1.tar"
    git = "https://github.com/Goddard-Fortran-Ecosystem/pFUnit.git"

    maintainers = ["mathomp4", "tclune", "citibeth"]

    version("4.6.1", sha256="19de22ff0542ca900aaf2957407f24d7dadaccd993ea210beaf22032d3095add")
    version("4.6.0", sha256="7c768ea3a2d16d8ef6229b25bd7756721c24a18db779c7422afde0e3e2248d72")
    version("4.5.0", sha256="ae0ed4541f2f4ec7b1d06eed532a49cb4c666394ab92b233911f92ce50f76743")
    version("4.4.1", sha256="6b5d5e19201f56e1ebc984f1cb30dffa0e9e1f14810aab601bd43e85fd3f18ab")
    version("4.4.0", sha256="e51e09b272e0f2598eb94cd1367158049deed1ac3a8779a7b30931e36f8c9752")
    version("4.3.0", sha256="a63d3ccda4a5e44b2afecbf3cc01275f80047602bd8587343a19f17db3e64b1d")
    version("4.2.7", sha256="1412134f812322b0aa5471007c9b7281fbe962e15b9efc9700cac24c9054bd84")
    version("4.2.6", sha256="9604d4c010a56bbb495eafcc9a2061a49572204dd211750b6f7209712c7c4a8a")
    version("4.2.5", sha256="a1f8edece98d6ffc3475465022828ccc9e26e2ecbd0374f4883bef626e33e549")
    version("4.2.3", sha256="9469a945a41649fd136bd75b3c5bae9895fe2d5f36046c24525b73d3d444d32f")
    version("4.2.2", sha256="f837b99585780c065e32249741926c61c8bf8b5b0b170ffc0fbcde105afbbb6a")
    version("4.2.1", sha256="977ac9de453da26700b7d4660f783e2850b6d4c9bbf36a4ffb721dbdeb8eb58c")
    version("4.2.0", sha256="33df62f80cf03827455508b67d53f820ddffa2ec0f1ba999790ff1f87592ce16")
    version("4.1.14", sha256="bada2be8d7e69ca1f16209ba92293fa1c06748b78534d71b24b2c825450a495f")
    version("4.1.13", sha256="f388e08c67c51cbfd9f3a3658baac912b5506d2fc651410cd34a21260c309630")
    version("4.1.12", sha256="7d71b0fb996497fe9a20eb818d02d596cd0d3cded1033a89a9081fbd925c68f2")
    version("4.1.11", sha256="16160bac223aaa3ed2b27e30287d25fdaec3cf6f2c570ebd8d61196e6aa6180f")
    version("4.1.10", sha256="051c35ad9678002943f4a4f2ab532a6b44de86ca414751616f93e69f393f5373")
    version("3.3.3", sha256="9f673b58d20ad23148040a100227b4f876458a9d9aee0f0d84a5f0eef209ced5")
    version("3.3.2", sha256="b1cc2e109ba602ea71bccefaa3c4a06e7ab1330db9ce6c08db89cfde497b8ab8")
    version("3.3.1", sha256="f8f4bea7de991a518a0371b4c70b19e492aa9a0d3e6715eff9437f420b0cdb45")
    version("3.3.0", sha256="4036ab448b821b500fbe8be5e3d5ab3e419ebae8be82f7703bcf84ab1a0ff862")
    version("3.2.10", sha256="b9debba6d0e31b682423ffa756531e9728c10acde08c4d8e1609b4554f552b1a")
    version("3.2.9", sha256="403f9a150865700c8b4240fd033162b8d3e8aeefa265c50c5a6fe14c455fbabc")

    variant("shared", default=True, description="Build shared library in addition to static")
    variant("mpi", default=False, description="Enable MPI")
    variant("use_comm_world", default=False, description="Enable MPI_COMM_WORLD for testing")
    variant("openmp", default=False, description="Enable OpenMP")
    variant("fhamcrest", default=False, description="Enable hamcrest support")
    variant("esmf", default=False, description="Enable esmf support")
    variant("docs", default=False, description="Build docs")

    variant(
        "max_array_rank",
        values=int,
        default=5,
        description="Max number of Fortran dimensions of array asserts",
    )

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    depends_on("python@2.7:", type=("build", "run"))  # python3 too!
    depends_on("mpi", when="+mpi")
    depends_on("esmf", when="+esmf")
    depends_on("m4", when="@4.1.5:", type="build")
    depends_on("fargparse")

    conflicts(
        "%gcc@:8.3.9",
        when="@4.0.0:",
        msg="pFUnit requires GCC 8.4.0 or newer",
    )

    # See https://github.com/Goddard-Fortran-Ecosystem/pFUnit/pull/179
    conflicts("+shared", when="@4.0.0:")
    conflicts("+use_comm_world", when="~mpi")
    patch("mpi-test.patch", when="@:3 +use_comm_world")

    def patch(self):
        # The package tries to put .mod files in directory ./mod;
        # spack needs to put them in a standard location:
        for file in glob.glob("*/CMakeLists.txt"):
            filter_file(r".*/mod($|[^\w].*)", "", file)

    def url_for_version(self, version):
        url_base = "https://github.com/Goddard-Fortran-Ecosystem/pFUnit"
        # Version 4.2.3+ has a v...
        if version >= Version("4.2.3"):
            url = url_base + "/releases/download/v{0}/pFUnit-v{0}.tar"
        # Then version down to 4.0.0 does not
        elif version >= Version("4"):
            url = url_base + "/releases/download/v{0}/pFUnit-{0}.tar"
        else:
            url = url_base + "/archive/{0}.tar.gz"

        return url.format(version)

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DPYTHON_EXECUTABLE=%s" % spec["python"].command,
            self.define_from_variant("BUILD_SHARED", "shared"),
            "-DCMAKE_Fortran_MODULE_DIRECTORY=%s" % spec.prefix.include,
            self.define_from_variant("BUILD_DOCS", "docs"),
            "-DMAX_ASSERT_RANK=%s" % spec.variants["max_array_rank"].value,
        ]

        if self.spec.satisfies("%gcc@10:"):
            args.append("-DCMAKE_Fortran_FLAGS_DEBUG=-g -O2 -fallow-argument-mismatch")

        if spec.satisfies("@4.0.0:"):
            args.append("-DSKIP_MPI=%s" % ("YES" if "~mpi" in spec else "NO"))
            args.append("-DSKIP_OPENMP=%s" % ("YES" if "~openmp" in spec else "NO"))
            args.append("-DSKIP_FHAMCREST=%s" % ("YES" if "~fhamcrest" in spec else "NO"))
            args.append("-DSKIP_ESMF=%s" % ("YES" if "~esmf" in spec else "NO"))
        else:
            args.append(self.define_from_variant("MPI", "mpi"))
            args.append(self.define_from_variant("OPENMP", "openmp"))

        if spec.satisfies("+mpi"):
            args.extend(
                ["-DMPI_USE_MPIEXEC=YES", "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc]
            )

        return args

    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        args = ["tests"]
        if self.spec.satisfies("+mpi"):
            args.append("MPI=YES")
        if self.spec.satisfies("+openmp"):
            args.append("OPENMP=YES")
        with working_dir(self.build_directory):
            make(*args)

    def compiler_vendor(self):
        vendors = {
            "%gcc": "GNU",
            "%clang": "GNU",
            "%intel": "Intel",
            "%pgi": "PGI",
            "%nag": "NAG",
            "%cce": "Cray",
        }
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                return value
        raise InstallError("Unsupported compiler.")

    def setup_build_environment(self, env):
        env.set("PFUNIT", self.spec.prefix)
        env.set("F90_VENDOR", self.compiler_vendor())

    def setup_run_environment(self, env):
        env.set("PFUNIT", self.spec.prefix)
        env.set("F90_VENDOR", self.compiler_vendor())

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("PFUNIT", self.spec.prefix)
        env.set("F90_VENDOR", self.compiler_vendor())
