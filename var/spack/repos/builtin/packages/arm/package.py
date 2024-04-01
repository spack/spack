# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Arm(Package, CompilerPackage):
    """Stub package for external detection of the ARM compiler package."""

    homepage = "https://developer.arm.com/downloads/-/arm-compiler-for-linux"
    url = "https://developer.arm.com/downloads/-/arm-compiler-for-linux"

    languages = ["c", "cxx", "fortran"]
    c_names = ["armclang"]
    cxx_names = ["armclang++"]
    fortran_names = ["armflang"]

    version_argument = "--version"
    version_regex = r"Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) "

    # notify when the package is updated.
    maintainers("becker33")

    version("12.0.0")

    def install(self, spec, prefix):
        raise NotImplementedError("apple-clang compiler must be configured as external")
