# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gcc(Package):
    homepage = "http://www.example.com/"
    has_code = False

    version("13.2.0")
    version("12.3.0")

    @classmethod
    def runtime_constraints(cls, *, compiler, pkg):
        pkg("*").depends_on(
            "gcc-runtime",
            when="%gcc",
            type="link",
            description="If any package uses %gcc, it depends on gcc-runtime",
        )
        pkg("*").depends_on(
            f"gcc-runtime@{str(compiler.version)}:",
            when=f"%{str(compiler.spec)}",
            type="link",
            description=f"If any package uses %{str(compiler.spec)}, "
            f"it depends on gcc-runtime@{str(compiler.version)}:",
        )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(f"@={str(compiler.version)}", when=f"%{str(compiler.spec)}")
