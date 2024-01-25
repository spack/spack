# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

from spack.package import *
from spack.pkg.builtin.netlib_scalapack import ScalapackBase


class Amdscalapack(ScalapackBase):
    """
    ScaLAPACK is a library of high-performance linear algebra routines
    for parallel distributed memory machines. It depends on external
    libraries including BLAS and LAPACK for Linear Algebra computations.

    AMD's optimized version of ScaLAPACK enables using BLIS and
    LibFLAME library that have optimized dense matrix functions and
    solvers for AMD EPYC processor family CPUs.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-ScaLAPACK license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/scalapack/eula/scalapack-libraries-4-1-eula.html
    https://www.amd.com/en/developer/aocl/scalapack/eula/scalapack-libraries-eula.html
    """

    _name = "amdscalapack"
    homepage = "https://www.amd.com/en/developer/aocl/scalapack.html"
    git = "https://github.com/amd/aocl-scalapack"

    maintainers("amd-toolchain-support")

    license("BSD-3-Clause-Open-MPI")

    version("4.1", sha256="b2e51c3604e5869d1faaef2e52c92071fcb3de1345aebb2ea172206622067ad9")
    version("4.0", sha256="f02913b5984597b22cdb9a36198ed61039a1bf130308e778dc31b2a7eb88b33b")
    version("3.2", sha256="9e00979bb1be39d627bdacb01774bc043029840d542fafc934d16fec3e3b0892")
    version("3.1", sha256="4c2ee2c44644a0feec0c6fc1b1a413fa9028f14d7035d43a398f5afcfdbacb98")
    version("3.0", sha256="6e6f3578f44a8e64518d276e7580530599ecfa8729f568303ed2590688e7096f")
    version("2.2", sha256="2d64926864fc6d12157b86e3f88eb1a5205e7fc157bf67e7577d0f18b9a7484c")

    variant("ilp64", default=False, description="Build with ILP64 support")

    conflicts("+ilp64", when="@:3.0", msg="ILP64 is supported from 3.1 onwards")
    requires("target=x86_64:", msg="AMD scalapack available only on x86_64")

    def url_for_version(self, version):
        vers = "https://github.com/amd/{0}/archive/{1}.tar.gz"
        if version >= Version("3.1"):
            return vers.format("aocl-scalapack", version)
        else:
            return vers.format("scalapack", version)

    def cmake_args(self):
        """cmake_args function"""
        args = super().cmake_args()
        spec = self.spec

        if not (
            spec.satisfies(r"%aocc@3.2:4.1")
            or spec.satisfies(r"%gcc@12.2:13.1")
            or spec.satisfies(r"%clang@15:16")
        ):
            tty.warn(
                "AOCL has been tested to work with the following compilers\
                    versions - gcc@12.2:13.1, aocc@3.2:4.1, and clang@15:16\
                    see the following aocl userguide for details: \
                    https://www.amd.com/content/dam/amd/en/documents/developer/version-4-1-documents/aocl/aocl-4-1-user-guide.pdf"
            )

        if spec.satisfies("%gcc@10:"):
            args.extend(["-DCMAKE_Fortran_FLAGS={0}".format("-fallow-argument-mismatch")])

        if spec.satisfies("%clang@16:"):
            args.extend(["-DCMAKE_Fortran_FLAGS={0}".format("-cpp -fno-implicit-none")])

        if spec.satisfies("@2.2"):
            args.extend(
                [
                    "-DUSE_DOTC_WRAPPER:BOOL=%s"
                    % ("ON" if spec.satisfies("%aocc ^amdblis") else "OFF")
                ]
            )

        # -DENABLE_ILP64:BOOL=ON
        args.extend([self.define_from_variant("ENABLE_ILP64", "ilp64")])

        # -DUSE_F2C:BOOL=ON
        args.extend([self.define("USE_F2C", spec.satisfies("@:3.0"))])

        if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%aocc@4.1.0:"):
            c_flags = []
            c_flags.append("-Wno-implicit-function-declaration")
            c_flags.append("-Wno-deprecated-non-prototype")
            c_flags.append("-Wno-incompatible-pointer-types")
            args.append(self.define("CMAKE_C_FLAGS", " ".join(c_flags)))

        # link libflame library
        args.extend(["-DLAPACK_LIBRARIES={0}".format(self.spec["lapack"].libs)])

        args.extend(
            [
                "-DLAPACK_FOUND=true",
                "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            ]
        )

        return args
