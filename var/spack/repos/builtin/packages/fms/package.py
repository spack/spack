# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fms(CMakePackage):
    """GFDL's Flexible Modeling System (FMS) is a software environment
    that supports the efficient development, construction, execution,
    and scientific interpretation of atmospheric, oceanic, and climate
    system models."""

    homepage = "https://github.com/NOAA-GFDL/FMS"
    url = "https://github.com/NOAA-GFDL/FMS/archive/refs/tags/2022.04.tar.gz"
    git = "https://github.com/NOAA-GFDL/FMS.git"

    maintainers = [
        "AlexanderRichert-NOAA",
        "Hang-Lei-NOAA",
        "edwardhartnett",
        "rem1776",
    ]

    version("2022.04", sha256="f741479128afc2b93ca8291a4c5bcdb024a8cbeda1a26bf77a236c0f629e1b03")
    version("2022.03", sha256="42d2ac53d3c889a8177a6d7a132583364c0f6e5d5cbde0d980443b6797ad4838")
    version("2022.02", sha256="ad4978302b219e11b883b2f52519e1ee455137ad947474abb316c8654f72c874")
    version("2022.01", sha256="a1cba1f536923f5953c28729a28e5431e127b45d6bc2c15d230939f0c02daa9b")
    version("2021.04", sha256="dcb4fe80cb3b7846f7cf89b812afff09a78a10261ea048a851f28935d6b241b1")
    version(
        "2021.03.01", sha256="1f70e2a57f0d01e80fceb9ca9ce9661f5c1565d0437ab67618c2c4dfea0da6e9"
    )
    version("2021.03", sha256="a9fb6e85f44ff79e6f9e61e65f42a5ffd38fa661fe1a3e4da6f85ffacd2697ac")
    version(
        "2021.02.01", sha256="9b11d9474d7c90464af66d81fb86c4798cfa309b9a0da20b0fccf33c4f65386b"
    )
    version("2021.02", sha256="db810b2452a6952239f064b52c0c5c58fc62126057982111b9fcd64f1b3bd879")
    version("2021.01", sha256="38c748e2edb94ffeb021095d8bde4d74b7834610ce0ef1dbb4dce353eeb5cd96")
    version(
        "2020.04.02", sha256="bd6ce752b1018d4418398f14b9fc486f217de76bcbaaf2cdbf4c43e0b3f39f69"
    )
    version(
        "2020.04.01", sha256="2c409242de7dea0cf29f8dbf7495698b6bcac1eeb5c4599a728bdea172ffe37c"
    )
    version(
        "2019.01.03", sha256="60a5181e883e141f2fdd4a30c535a788d609bcbbbca4af7e1ec73f66f4e58dc0"
    )

    # DH* 20220602
    # These versions were adapated by JCSDA and are only meant to be
    # used temporarily, until the JCSDA changes have found their way
    # back into the official repository.
    # Commit corresponds to branch="release-stable" in the JCSDA public fork
    version("release-jcsda", commit="1f739141ef8b000a0bd75ae8bebfadea340299ba", no_cache=True)
    # version("dev-jcsda", branch="dev/jcsda", no_cache=True)

    with when("@release-jcsda"):
        git = "https://github.com/JCSDA/fms.git"
    # *DH 20220602

    variant(
        "64bit",
        default=True,
        description="Build a version of the library with default 64 bit reals",
    )
    variant("gfs_phys", default=True, description="Use GFS Physics")
    variant("openmp", default=True, description="Use OpenMP")
    variant("quad_precision", default=True, description="quad precision reals")
    variant(
        "yaml",
        default=False,
        description="yaml input file support(requires libyaml)",
        when="@2021.04:",
    )
    variant(
        "constants",
        default="GFDL",
        description="Build with <X> constants parameter definitions",
        values=("GFDL", "GEOS", "GFS"),
        multi=False,
        when="@2022.02:",
    )
    variant(
        "fpic", default=False, description="Build with position independent code", when="@2022.02:"
    )

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("mpi")
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    depends_on("libyaml", when="+yaml")

    # DH* 20220602
    depends_on("ecbuild", type=("build"), when="@release-jcsda")
    depends_on("jedi-cmake", type=("build"), when="@release-jcsda")
    # *DH 20220602

    def cmake_args(self):
        args = [
            self.define_from_variant("64BIT"),
            self.define_from_variant("GFS_PHYS"),
            self.define_from_variant("OPENMP"),
            self.define_from_variant("ENABLE_QUAD_PRECISION", "quad_precision"),
            self.define_from_variant("WITH_YAML", "yaml"),
            self.define_from_variant("CONSTANTS"),
            self.define_from_variant("FPIC"),
        ]

        args.append(self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc))
        args.append(self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx))
        args.append(self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc))

        fflags = []

        if self.compiler.name in ["gcc", "clang", "apple-clang"]:
            gfortran_major_version = int(spack.compiler.get_compiler_version_output(
                self.compiler.fc, "-dumpversion").split(".")[0])

            if gfortran_major_version >= 10:
                fflags.append("-fallow-argument-mismatch")

        if fflags:
            args.append(self.define('CMAKE_Fortran_FLAGS', ' '.join(fflags)))

        return args
