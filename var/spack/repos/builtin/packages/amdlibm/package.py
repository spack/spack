# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Amdlibm(SConsPackage):
    """AMD LibM is a software library containing a collection of basic math
    functions optimized for x86-64 processor-based machines. It provides
    many routines from the list of standard C99 math functions.
    Applications can link into AMD LibM library and invoke math functions
    instead of compiler's math functions for better accuracy and
    performance.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-FFTW license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/libm/libm-4-0-eula.html
    https://www.amd.com/en/developer/aocl/libm/libm-eula.html
    """

    _name = "amdlibm"
    homepage = "https://developer.amd.com/amd-aocl/amd-math-library-libm/"
    git = "https://github.com/amd/aocl-libm-ose.git"
    url = "https://github.com/amd/aocl-libm-ose/archive/refs/tags/3.0.tar.gz"
    maintainers("amd-toolchain-support")

    version("4.0", sha256="038c1eab544be77598eccda791b26553d3b9e2ee4ab3f5ad85fdd2a77d015a7d")
    version("3.2", sha256="c75b287c38a3ce997066af1f5c8d2b19fc460d5e56678ea81f3ac33eb79ec890")
    version("3.1", sha256="dee487cc2d89c2dc93508be2c67592670ffc1d02776c017e8907317003f48845")
    version("3.0", sha256="eb26b5e174f43ce083928d0d8748a6d6d74853333bba37d50057aac2bef7c7aa")
    version("2.2", commit="4033e022da428125747e118ccd6fdd9cee21c470")

    variant("verbose", default=False, description="Building with verbosity")

    # Mandatory dependencies
    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("scons@3.1.2:", type=("build"))
    depends_on("mpfr", type=("link"))

    patch("0001-libm-ose-Scripts-cleanup-pyc-files.patch", when="@2.2")
    patch("0002-libm-ose-prevent-log-v3.c-from-building.patch", when="@2.2")

    conflicts("%gcc@:9.1.0", msg="Minimum supported GCC version is 9.2.0")
    conflicts("%gcc@12.2.0:", msg="Maximum supported GCC version is 12.1.0")
    conflicts("%clang@9:", msg="Minimum supported Clang version is 9.0.0")
    conflicts("%aocc@3.2.0", msg="dependency on python@3.6.2")

    def build_args(self, spec, prefix):
        """Setting build arguments for amdlibm"""
        args = ["--prefix={0}".format(prefix)]

        # we are circumventing the use of
        # Spacks compiler wrappers because
        # SCons wipes out all environment variables.
        if self.spec.satisfies("@:3.0 %aocc"):
            args.append("--compiler=aocc")

        var_prefix = "" if self.spec.satisfies("@:3.0") else "ALM_"
        args.append("{0}CC={1}".format(var_prefix, self.compiler.cc))
        args.append("{0}CXX={1}".format(var_prefix, self.compiler.cxx))

        if "+verbose" in self.spec:
            args.append("--verbose=1")
        else:
            args.append("--verbose=0")

        return args

    install_args = build_args

    @run_after("install")
    def create_symlink(self):
        """Symbolic link for backward compatibility"""
        with working_dir(self.prefix.lib):
            os.symlink("libalm.a", "libamdlibm.a")
            os.symlink("libalm.so", "libamdlibm.so")
            if self.spec.satisfies("@4.0:"):
                os.symlink("libalmfast.a", "libamdlibmfast.a")
                os.symlink("libalmfast.so", "libamdlibmfast.so")
