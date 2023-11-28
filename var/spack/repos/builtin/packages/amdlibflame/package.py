# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------\
import os

from llnl.util import tty

from spack.package import *
from spack.pkg.builtin.libflame import LibflameBase


class Amdlibflame(LibflameBase):
    """libFLAME (AMD Optimized version) is a portable library for
    dense matrix computations, providing much of the functionality
    present in Linear Algebra Package (LAPACK). It includes a
    compatibility layer, FLAPACK, which includes complete LAPACK
    implementation.

    The library provides scientific and numerical computing communities
    with a modern, high-performance dense linear algebra library that is
    extensible, easy to use, and available under an open source
    license. libFLAME is a C-only implementation and does not
    depend on any external FORTRAN libraries including LAPACK.
    There is an optional backward compatibility layer, lapack2flame
    that maps LAPACK routine invocations to their corresponding
    native C implementations in libFLAME. This allows legacy
    applications to start taking advantage of libFLAME with
    virtually no changes to their source code.

    In combination with BLIS library which includes optimizations
    for the AMD EPYC processor family, libFLAME enables running
    high performing LAPACK functionalities on AMD platform.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-libFLAME license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/dense/eula-libflame/libflame-4-1-eula.html
    https://www.amd.com/en/developer/aocl/dense/eula-libflame/libflame-eula.html
    """

    _name = "amdlibflame"
    homepage = "https://www.amd.com/en/developer/aocl/blis.html#libflame"
    url = "https://github.com/amd/libflame/archive/3.0.tar.gz"
    git = "https://github.com/amd/amdlibflame"

    maintainers("amd-toolchain-support")

    version("4.1", sha256="8aed69c60d11cc17e058cabcb8a931cee4f343064ade3e73d3392b7214624b61")
    version("4.0", sha256="bcb05763aa1df1e88f0da5e43ff86d956826cbea1d9c5ff591d78a3e091c66a4")
    version("3.2", sha256="6b5337fb668b82d0ed0a4ab4b5af4e2f72e4cedbeeb4a8b6eb9a3ef057fb749a")
    version("3.1", sha256="4520fb93fcc89161f65a40810cae0fa1f87cecb242da4a69655f502545a53426")
    version("3.0.1", sha256="5859e7b39ffbe73115dd598b035f212d36310462cf3a45e555a5087301710776")
    version("3.0", sha256="d94e08b688539748571e6d4c1ec1ce42732eac18bd75de989234983c33f01ced")
    version("2.2", sha256="12b9c1f92d2c2fa637305aaa15cf706652406f210eaa5cbc17aaea9fcfa576dc")

    variant("ilp64", default=False, description="Build with ILP64 support")

    conflicts("+ilp64", when="@:3.0.0", msg="ILP64 is supported from 3.0.1 onwards")
    conflicts("threads=pthreads", msg="pthread is not supported")
    conflicts("threads=openmp", when="@:3", msg="openmp is not supported by amdlibflame < 4.0")

    patch("aocc-2.2.0.patch", when="@:2", level=1)
    patch("cray-compiler-wrapper.patch", when="@:3.0.0", level=1)
    patch("supermat.patch", when="@4.0:4.1", level=1)

    provides("flame@5.2", when="@2:")

    depends_on("python+pythoncmd", type="build")
    depends_on("gmake@4:", when="@3.0.1,3.1:", type="build")
    depends_on("aocl-utils", type=("build"), when="@4.1: ")

    @property
    def lapack_libs(self):
        """find lapack_libs function"""
        return find_libraries(
            "libflame", root=self.prefix, shared="+shared" in self.spec, recursive=True
        )

    @property
    def libs(self):
        """find libflame libs function"""
        return find_libraries(
            "libflame", root=self.prefix, shared="+shared" in self.spec, recursive=True
        )

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%aocc@4.1.0:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
                flags.append("-Wno-implicit-function-declaration")
                flags.append("-Wno-sometimes-uninitialized")
        return (flags, None, None)

    def configure_args(self):
        """configure_args function"""
        args = super().configure_args()

        if not (
            self.spec.satisfies(r"%aocc@3.2:4.1")
            or self.spec.satisfies(r"%gcc@12.2:13.1")
            or self.spec.satisfies(r"%clang@15:16")
        ):
            tty.warn(
                "AOCL has been tested to work with the following compilers\
                    versions - gcc@12.2:13.1, aocc@3.2:4.1, and clang@15:16\
                    see the following aocl userguide for details: \
                    https://www.amd.com/content/dam/amd/en/documents/developer/version-4-1-documents/aocl/aocl-4-1-user-guide.pdf"
            )

        # From 3.2 version, amd optimized flags are encapsulated under:
        # enable-amd-aocc-flags for AOCC compiler
        # enable-amd-flags for all other compilers
        if "@3.2:" in self.spec:
            if "%aocc" in self.spec:
                args.append("--enable-amd-aocc-flags")
            else:
                args.append("--enable-amd-flags")

        if "@:3.1" in self.spec:
            args.append("--enable-external-lapack-interfaces")

        if "@3.1" in self.spec:
            args.append("--enable-blas-ext-gemmt")

        if "@3.1 %aocc" in self.spec:
            args.append("--enable-void-return-complex")

        if "@3.0:3.1 %aocc" in self.spec:
            """To enabled Fortran to C calling convention for
            complex types when compiling with aocc flang"""
            args.append("--enable-f2c-dotc")

        if "@3.0.1: +ilp64" in self.spec:
            args.append("--enable-ilp64")

        if "@4.1:" in self.spec:
            args.append("CFLAGS=-I{0}".format(self.spec["aocl-utils"].prefix.include))
            aocl_utils_lib_path = os.path.join(
                self.spec["aocl-utils"].prefix.lib, "libaoclutils.a"
            )
            args.append("LIBAOCLUTILS_LIBRARY_PATH={0}".format(aocl_utils_lib_path))

        return args

    @when("@4.1:")
    def build(self, spec, prefix):
        aocl_utils_lib_path = os.path.join(self.spec["aocl-utils"].prefix.lib, "libaoclutils.a")
        make("all", "LIBAOCLUTILS_LIBRARY_PATH={0}".format(aocl_utils_lib_path))

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        """make check for single and multithread"""
        blas_flags = self.spec["blas"].libs.ld_flags
        if self.spec.variants["threads"].value != "none":
            make("check", "LIBBLAS = -fopenmp {0}".format(blas_flags), parallel=False)
        else:
            make("check", "LIBBLAS = {0}".format(blas_flags), parallel=False)

    def install(self, spec, prefix):
        """make install function"""
        # make install in parallel fails with message 'File already exists'
        make("install", parallel=False)
