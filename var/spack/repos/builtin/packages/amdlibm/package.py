# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amdlibm(SConsPackage):
    """AMD LibM is a software library containing a collection of basic math
    functions optimized for x86-64 processor-based machines. It provides
    many routines from the list of standard C99 math functions.
    Applications can link into AMD LibM library and invoke math functions
    instead of compiler's math functions for better accuracy and
    performance."""

    homepage = "https://developer.amd.com/amd-aocl/amd-math-library-libm/"
    git = "https://github.com/amd/aocl-libm-ose.git"
    maintainers = ["amd-toolchain-support"]

    # Download and build from latest source
    version("master", branch="master")

    variant("debug", default=False,
            description="Building with debug")
    variant("verbose", default=False,
            description="Building with verbosity")

    # Mandatory dependencies
    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("scons@3.1.2:", type=("build"))
    depends_on("mpfr", type=("build"))

    patch('0001-libm-ose-Scripts-cleanup-pyc-files.patch')
    patch('0002-libm-ose-prevent-log-v3.c-from-building.patch')

    conflicts("%gcc@:9.1.999", msg="Minimum required GCC version is 9.2.0")

    def build_args(self, spec, prefix):
        """Setting build arguments for amdlibm """
        args = ["--prefix={0}".format(prefix)]

        if "%aocc" in spec:
            args.append("--compiler=aocc")
            args.append("CC={0}".format(self.compiler.cc))
            args.append("CXX={0}".format(self.compiler.cxx))
        else:
            args.append("CC={0}".format(self.compiler.cc))
            args.append("CXX={0}".format(self.compiler.cxx))

        if "+verbose" in spec:
            args.append("verbose=1")
        else:
            args.append("verbose=0")

        return args

    def install_args(self, spec, prefix):
        """Setting install arguments for amdlibm """
        args = [
            "--prefix={0}".format(prefix),
        ]

        if "%aocc" in spec:
            args.append("--compiler=aocc")
            args.append("CC={0}".format(self.compiler.cc))
            args.append("CXX={0}".format(self.compiler.cxx))
        else:
            args.append("CC={0}".format(self.compiler.cc))
            args.append("CXX={0}".format(self.compiler.cxx))

        if "+verbose" in spec:
            args.append("verbose=1")
        else:
            args.append("verbose=0")

        return args
