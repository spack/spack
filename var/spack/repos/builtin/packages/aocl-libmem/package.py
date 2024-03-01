# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
from llnl.util import tty

from spack.package import *


class AoclLibmem(CMakePackage):
    """
    AOCL-LibMem is a Linux library of data movement and manipulation
    functions (such as memcpy and strcpy) highly optimized for AMD Zen
    micro-architecture.

    This library has multiple implementations of each function that can be
    chosen based on the application requirements as per alignments, instruction
    choice, threshold values, and tunable parameters.

    By default, this library will choose the best fit implementation based on
    the underlying micro-architectural support for CPU features and instructions.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-LibMem license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/libmem/eula/libmem-4-2-eula.html
    """

    _name = "aocl-libmem"
    homepage = "https://www.amd.com/en/developer/aocl/libmem.html"
    git = "https://github.com/amd/aocl-libmem"
    url = "https://github.com/amd/aocl-libmem/archive/refs/tags/4.2.tar.gz"

    maintainers("amd-toolchain-support")

    version(
        "4.2",
        sha256="4ff5bd8002e94cc2029ef1aeda72e7cf944b797c7f07383656caa93bcb447569",
        preferred=True,
    )

    variant("logging", default=False, description="Enable/Disable logger")
    variant("tunables", default=False, description="Enable/Disable user input")
    variant("shared", default=True, description="build shared library")
    variant(
        "vectorization",
        default="auto",
        description="Use hardware vectorization support",
        values=("avx2", "avx512", "auto"),
        multi=False,
    )

    depends_on("cmake@3.15:", type="build")

    @property
    def libs(self):
        """find libmem libs function"""
        shared = "+shared" in self.spec
        return find_libraries("libaocl-libmem", root=self.prefix, recursive=True, shared=shared)

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec

        if not (
            spec.satisfies(r"%aocc@4.1:4.2")
            or spec.satisfies(r"%gcc@12.2:13.1")
            or spec.satisfies(r"%clang@16:17")
        ):
            tty.warn(
                "AOCL has been tested to work with the following compilers "
                "versions - gcc@12.2:13.1, aocc@4.1:4.2, and clang@16:17 "
                "see the following aocl userguide for details: "
                "https://www.amd.com/content/dam/amd/en/documents/developer/version-4-2-documents/aocl/aocl-4-2-user-guide.pdf"
            )

        args = []
        args.append(self.define_from_variant("ENABLE_LOGGING", "logging"))
        args.append(self.define_from_variant("ENABLE_TUNABLES", "tunables"))
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        if spec.satisfies("vectorisation=auto"):
            if "avx512" in self.spec.target:
                args.append("-ALMEM_ARCH=avx512")
            elif "avx2" in self.spec.target:
                args.append("-ALMEM_ARCH=avx2")
            else:
                args.append("-ALMEM_ARCH=none")
        else:
            args.append(self.define("ALMEM_ARCH", spec.variants["vectorization"].value))
        return args
