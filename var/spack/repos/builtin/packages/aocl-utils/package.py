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
    https://www.amd.com/en/developer/aocl/utils/utils-eula/utils-eula-4-1.html
    """

    _name = "aocl-utils"
    homepage = "https://www.amd.com/en/developer/aocl/utils.html"
    url = "https://github.com/amd/aocl-utils/archive/refs/tags/4.1.tar.gz"
    git = "https://github.com/amd/aocl-utils"

    maintainers("amd-toolchain-support")

    license("BSD-3-Clause")

    version("4.1", sha256="a2f271f5eef07da366dae421af3c89286ebb6239047a31a46451758d4a06bc85")

    variant("doc", default=False, description="enable documentation")
    variant("tests", default=False, description="enable testing")
    variant("examples", default=False, description="enable examples")

    depends_on("doxygen", when="+doc")

    def cmake_args(self):
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

        args = []
        args.append(self.define_from_variant("ALCI_DOCS", "doc"))
        args.append(self.define_from_variant("ALCI_TESTS", "tests"))
        args.append(self.define_from_variant("ALCI_EXAMPLES", "examples"))

        return args
