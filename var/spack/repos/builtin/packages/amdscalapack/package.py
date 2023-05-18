# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    https://www.amd.com/en/developer/aocl/scalapack/scalapack-libraries-4-0-eula.html
    https://www.amd.com/en/developer/aocl/scalapack/scalapack-libraries-eula.html
    """

    _name = "amdscalapack"
    homepage = "https://developer.amd.com/amd-aocl/scalapack/"
    git = "https://github.com/amd/scalapack.git"

    maintainers("amd-toolchain-support")

    version("4.0", sha256="f02913b5984597b22cdb9a36198ed61039a1bf130308e778dc31b2a7eb88b33b")
    version("3.2", sha256="9e00979bb1be39d627bdacb01774bc043029840d542fafc934d16fec3e3b0892")
    version("3.1", sha256="4c2ee2c44644a0feec0c6fc1b1a413fa9028f14d7035d43a398f5afcfdbacb98")
    version("3.0", sha256="6e6f3578f44a8e64518d276e7580530599ecfa8729f568303ed2590688e7096f")
    version("2.2", sha256="2d64926864fc6d12157b86e3f88eb1a5205e7fc157bf67e7577d0f18b9a7484c")

    variant("ilp64", default=False, description="Build with ILP64 support")

    conflicts("+ilp64", when="@:3.0", msg="ILP64 is supported from 3.1 onwards")

    def url_for_version(self, version):
        vers = "https://github.com/amd/{0}/archive/{1}.tar.gz"
        if version >= Version("3.1"):
            return vers.format("aocl-scalapack", version)
        else:
            return vers.format("scalapack", version)

    def cmake_args(self):
        """cmake_args function"""
        args = super(Amdscalapack, self).cmake_args()
        spec = self.spec

        if spec.satisfies("%gcc@10:"):
            args.extend(["-DCMAKE_Fortran_FLAGS={0}".format("-fallow-argument-mismatch")])

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

        args.extend(
            [
                "-DLAPACK_FOUND=true",
                "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            ]
        )

        return args
