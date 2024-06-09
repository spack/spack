# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

from spack.package import *


class AoclUtils(CMakePackage):
    """The library AOCL-Utils is intended to provide a uniform interface to all
    AOCL libraries to access CPU features, especially for AMD CPUs. The library
    provides the following features:
    * Core details
    * Flags available/usable
    * ISA available/usable
    * Topology about L1/L2/L3
    AOCL-Utils is designed to be integrated into other AMD AOCL libraries. Each
    project has their own mechanism to identify CPU and provide necessary
    features such as "dynamic dispatch".The main purpose of this library is to
    provide a centralized mechanism to update/validate and provide information
    to the users of this library.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-Utils license
    agreement. You may obtain a copy of this license agreement from
    https://www.amd.com/content/dam/amd/en/documents/developer/version-4-2-eulas/utils-elua-4-2.pdf
    """

    _name = "aocl-utils"
    homepage = "https://www.amd.com/en/developer/aocl/utils.html"
    url = "https://github.com/amd/aocl-utils/archive/refs/tags/4.1.tar.gz"
    git = "https://github.com/amd/aocl-utils"

    maintainers("amd-toolchain-support")

    license("BSD-3-Clause")

    version(
        "4.2",
        sha256="1294cdf275de44d3a22fea6fc4cd5bf66260d0a19abb2e488b898aaf632486bd",
        preferred=True,
    )
    version("4.1", sha256="660746e7770dd195059ec25e124759b126ee9f060f43302d13354560ca76c02c")

    variant("doc", default=False, description="enable documentation")
    variant("tests", default=False, description="enable testing")
    variant("shared", default=True, when="@4.2:", description="build shared library")
    variant("examples", default=False, description="enable examples")

    depends_on("doxygen", when="+doc")

    @property
    def libs(self):
        """find aocl-utils libs function"""
        shared = "+shared" in self.spec
        return find_libraries("libaoclutils", root=self.prefix, recursive=True, shared=shared)

    def cmake_args(self):
        spec = self.spec
        if not (
            spec.satisfies(r"%aocc@3.2:4.2")
            or spec.satisfies(r"%gcc@12.2:13.1")
            or spec.satisfies(r"%clang@15:17")
        ):
            tty.warn(
                "AOCL has been tested to work with the following compilers "
                "versions - gcc@12.2:13.1, aocc@3.2:4.2, and clang@15:17 "
                "see the following aocl userguide for details: "
                "https://www.amd.com/content/dam/amd/en/documents/developer/version-4-2-documents/aocl/aocl-4-2-user-guide.pdf"
            )

        args = []
        args.append(self.define_from_variant("ALCI_DOCS", "doc"))
        args.append(self.define_from_variant("ALCI_TESTS", "tests"))
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("ALCI_EXAMPLES", "examples"))

        return args
